---
ID: umd-whpool-0003
Status: Accepted
Date: 2024-06-04
Author: Tim Kanke <tkanke@umd.edu>

---

# CKEditor Read Only Mode

## Context

We need to decide how to have CKEditor not make changes for the Original Body field on the Item View page.

## Decision Drivers

* Be easy for the user to understand what is not editable
* Be a consitent implementation for message bodies
* Allow WYSIWYG and source editing

## Considered Options

1. Use CKEditor read only mode
2. Prevent changes from being saved and add a disclaimer stating this fact
3. Replace Body Original field with separate tabbed display of WYSIWYG and source text

## Decision

Chosen option: Prevent changes from being saved and add a disclaimer stating this fact. Due to the fact that source editing is implemented with a plugin, it has to be added as an exception to read only mode. This creates a potentially confusing situation where a user can edit text in source editing mode but not in WYSIWYG mode. Furthermore, read only mode has yet to be added to the Django integration library Django-CKEditor-5.

## Pros and Cons of the Options

### Use CKEditor read only mode

* Good, because it keeps users from editing text in WYSIWYG mode
* Good, because it makes it clear that the text is not editable
* Bad, because it does not keep users from editing text via the source editing plugin
* Bad, because it has yet to be implemented in the Django integration library Django-CKEditor-5

### Prevent changes from being saved and add a disclaimer stating this fact

* Good, because it keeps unintentional changes from being saved to the database
* Good, because it keeps the same editing window experience
* Bad, because it appears that users are able to make changes

### Replace Body Original field with separate tabbed display of WYSIWYG and source text

* Good, because it makes it clear that the text is not editable
* Bad, because it does not keep a consitent experience between body fields
