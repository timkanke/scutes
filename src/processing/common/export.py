import logging
import zipfile

from bs4 import BeautifulSoup
from csv import DictWriter
from pathlib import Path

from processing.models import Batch, File, Item


logger = logging.getLogger(__name__)

HEADER = ['Identifier', 'Title', 'Date', 'Creator', 'Format', 'Rights Statement', 'FILES', 'Object Type']


def convert_body_img_src(body_final):
    soup = BeautifulSoup(body_final, 'lxml')
    imgs = soup.find_all('img')
    for img in imgs:
        img_url = img['src']
        new_url = img_url.strip('/')
        img['src'] = new_url

    body_final = str(soup)
    return body_final


def export(batch_selected, export_path):
    batch = Batch.objects.get(id=batch_selected)
    batch_selected_name = batch.name

    # Check if all items are reviewed
    total_items_count = Item.objects.filter(batch=batch_selected).count()
    items_completed = Item.objects.filter(batch=batch_selected, review_status=2)
    items_in_progress = Item.objects.filter(batch=batch_selected, review_status=1)
    items_not_started = Item.objects.filter(batch=batch_selected, review_status=0)

    items_reviewed_count = items_completed.count()
    not_reviewed_count = items_in_progress.count() + items_not_started.count()

    if items_reviewed_count != 0:
        logger.info('Not all items in this batch have been reviewed.')
        logger.info(f'Number of items not reviewed: {not_reviewed_count} out of {total_items_count}')
        yield '<div class="text-bg-danger p-3">Warning! Not all items in this batch have been reviewed.</div>'
        yield f'<div class="text-bg-warning p-3">Number of items not reviewed: {not_reviewed_count} out of {total_items_count} items.<br>'
        yield f'Number of items in progress: {items_in_progress.count()}<br>'
        yield f'Number of items not started: {items_not_started.count()}</div>'

    # Select items only in selected batch and marked publish
    items = Item.objects.filter(batch=batch_selected, publish=True)

    # Create output path if not exists
    path = Path(export_path, batch_selected_name)
    path.mkdir(parents=True, exist_ok=True)
    output_path = path

    # Open the output CSV for writing
    with open(output_path / 'whpool.csv', 'w') as csv_file:
        csv_writer = DictWriter(csv_file, fieldnames=HEADER, extrasaction='ignore', escapechar='\\')
        # Add the headers
        csv_writer.writeheader()
        # Iterate over items in database
        for item in items:
            logger.info(f'Exporting: {item.id}, {item.title}')
            yield f'Exporting: {item.id}, {item.title}<br>'

            # Create HTML file
            id = str(item.id)
            body_name = 'body-' + id + '.html'
            body = Path(output_path / id / body_name)
            body.parent.mkdir(parents=True, exist_ok=True)
            body_final = item.body_final
            body_final = convert_body_img_src(body_final)
            with open(body, 'w') as body:
                body.write(body_final)

            # Create media file(s)
            csv_files_path = []
            files = File.objects.filter(item=item)
            for file in files:
                file_name = file.file.name
                if file.disposition == 'attachment':
                    file_type = 'attachment'
                elif file.disposition == 'inline':
                    file_type = 'media'
                elif file.disposition == 'external':
                    file_type = 'media'
                else:
                    pass

                file_path = Path(output_path / id / file_type / file_name)
                csv_file_path = id + '/' + file_type + '/' + file_name
                csv_files_path.append(csv_file_path)
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_to_download = file.file.read()
                with open(file_path, 'wb') as f:
                    f.write(file_to_download)

            # Write CSV row
            csv_writer.writerow(
                {
                    'Identifier': item.id,
                    'Title': item.title,
                    'Date': item.date,
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
    yield f'Finished export of {batch_selected_name}'
