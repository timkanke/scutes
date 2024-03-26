import logging
import re
import zipfile

from bs4 import BeautifulSoup
from csv import DictWriter
from pathlib import Path

from django.utils import timezone
from processing.models import Batch, File, Item
from scutes.settings import KEEP_EXPORT_DIRECTORIES, EXPORT_PATH


logger = logging.getLogger(__name__)

HEADER = ['Identifier', 'Title', 'Date', 'Creator', 'Format', 'Rights Statement', 'FILES', 'Object Type']


def redact_final(html):
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find_all('del', {'class': 'redacted'})

    for tag in tags:
        new_string = '▊▊▊▊▊▊▊▊▊▊'
        tag = tag.replace_with(new_string)

    html = str(soup)
    return html


def rm_tree(pth: Path):
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


def convert_and_export(batch_selected):
    # Convert marked redactions
    items = Item.objects.filter(batch=batch_selected)
    item = Item.objects.all()
    logger.info(f'Converting Batch {batch_selected}')
    yield f'<div class="text-bg-info p-3">Converting Batch {batch_selected}</div>'
    for item in items:
        logger.info(f'Converting: {item.id}, {item.title}')
        yield f'Converting: {item.id}, {item.title}<br>'
        html = item.body_redact
        html = redact_final(html)
        item.body_final = html
        item.save(update_fields=['body_final'])
    yield f'<div class="text-bg-success p-3">Completed Converting Batch {batch_selected}</div>'

    # export
    batch = Batch.objects.get(id=batch_selected)
    batch_selected_name = batch.name

    yield f'<div class="text-bg-info p-3">Exporting Batch {batch_selected}</div>'

    # Select items only in selected batch and marked publish
    items = Item.objects.filter(batch=batch_selected, publish=True)

    # Create output path if not exists
    path = Path(EXPORT_PATH, batch_selected_name)
    if path.is_dir():
        rm_tree(path)

    path.mkdir(parents=True, exist_ok=True)
    output_path = path

    # Open the output CSV for writing
    with open(output_path / 'whpool.csv', 'w') as csv_file:
        csv_writer = DictWriter(csv_file, fieldnames=HEADER, extrasaction='ignore', escapechar='\\')
        csv_writer.writeheader()
        for item in items:
            logger.info(f'Exporting: {item.id}, {item.title}')
            yield f'Exporting: {item.id}, {item.title}<br>'

            # Create directory
            item_id = str(item.id)
            body_name = 'body-' + item_id + '.html'
            body = Path(output_path / item_id / body_name)
            body.parent.mkdir(parents=True, exist_ok=True)

            csv_files_path = []
            body_path = item_id + '/' + body_name
            csv_files_path.append(body_path)
            body_final = item.body_final
            soup = BeautifulSoup(body_final, 'lxml')

            # Create media file(s)
            files = File.objects.filter(item=item)
            for file in files:
                file_name = file.file.name[6:]
                file_path = Path(item_id) / str(file.disposition) / file_name
                output_file = Path(output_path) / file_path
                csv_files_path.append(str(file_path))
                output_file.parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, 'wb') as f:
                    f.write(file.file.read())

                # Convert img src
                if file.disposition != 'attachment':
                    img_file = '/media/' + file.file.name
                    img = soup.find('img', src=img_file)
                    new_src = str(file.disposition) + '/' + file_name
                    img['src'] = new_src

            # Create HTML file
            body_final = str(soup)
            with open(body, 'w') as body:
                body.write(body_final)

            # Convert timedate to EDTF
            timestamp = item.date.isoformat()
            # work around a parse_edtf bug where it does not accept "+00:00" or "-00:00"
            # as a valid timezone offset, by changing those to "Z"
            timestamp = re.sub('[+-]00:00$', 'Z', timestamp)

            # Write CSV row
            csv_writer.writerow(
                {
                    'Identifier': batch_selected_name.replace('-', '') + '_' + str(item.id),
                    'Title': item.title,
                    'Date': timestamp,
                    'Creator': item.reporter,
                    'Format': 'http://vocab.lib.umd.edu/form#pool_reports',
                    'Rights Statement': 'http://vocab.lib.umd.edu/rightsStatement#InC-NC',
                    'FILES': ';'.join(csv_files_path),
                    'Object Type': 'http://purl.org/dc/dcmitype/Text',
                }
            )

    # Zip directory
    directory = Path(output_path)
    logger.info(f'Creating zip file for {directory}')
    yield f'Creating zip file for {batch_selected_name}<br>'
    zip_file_name = batch_selected_name + '.zip'
    zip_file = Path(directory.parent / zip_file_name)
    with zipfile.ZipFile(zip_file, mode='w') as archive:
        for file_path in directory.rglob('*'):
            archive.write(file_path, arcname=file_path.relative_to(directory))
    yield f'<div class="text-bg-success p-3">Finished export of {batch_selected_name}</div>'

    if KEEP_EXPORT_DIRECTORIES is False:
        rm_tree(path)

    batch.last_export = timezone.now()
    batch.save()

    # Notify if all items are reviewed
    total_items_count = Item.objects.filter(batch=batch_selected).count()
    items_completed_count = Item.objects.filter(batch=batch_selected, review_status=2).count()
    not_reviewed_count = total_items_count - items_completed_count

    if not_reviewed_count != 0:
        logger.info('Not all items in this batch have been reviewed.')
        logger.info(f'Number of items not reviewed: {not_reviewed_count} out of {total_items_count}')
        yield '<div class="text-bg-danger p-3">Warning! Not all items in this batch have been reviewed.</div>'
        yield f'<div class="text-bg-warning p-3">Number of items not reviewed: {not_reviewed_count} out of {total_items_count} items.<br></div>'
