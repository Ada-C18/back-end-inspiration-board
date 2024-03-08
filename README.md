## Overview
Part of a full-stack project involving four team members. Completed in 8 days (including planning time) over three weeks.<br /><br />
**Front-end owners:** [@kalawac](https://github.com/kalawac/), [@annalord](https://github.com/annalord/)<br />
**Back-end owners:** [@emilyiscoding](https://github.com/EmilyIsCoding/), [@bukunmig](https://github.com/BukunmiG/)<br />
### Related Links
- [Deployed project](http://hackspoboard.herokuapp.com/)
- [Front-end repo](https://github.com/kalawac/front-end-inspiration-board)<br />
- [Back-end repo](https://github.com/EmilyIsCoding/back-end-inspiration-board/)<br />
- [Ada C-18 repo with general full-stack project overview and requirements](https://github.com/Ada-C18/full-stack-inspiration-board)

# Inspiration Board: Back-end Layer

This scaffold includes the following:

## `app/__init__.py`

This file configures the app. It's where:

We expect developers to modify this file by:

- Replacing the database connection string
- Importing all models
- Registering all blueprints

Note that `create_app` also uses CORS. There is no extra action needed to be done with CORS.

## `app/routes.py`

We expect endpoints to be defined here.

The file already imports:

- `Blueprint`
- `request`
- `jsonify`
- `make_response`
- `db`

Feel free to alter these import statements.

This file also has a comment to define a Blueprint. Feel free to delete it.

## `app/models` Directory

This project already includes `app/models/board.py` and `app/models/card.py`, to anticipate the models `Board` and `Card`.

Both files already import `db`, for convenience!

## `requirements.txt`

This file lists the dependencies we anticipate are needed for the project.

## `Procfile`

This file already has the contents needed for a Heroku deployment.

If the `create_app` function in `app/__init__.py` is renamed or moved, the contents of this file need to change. Otherwise, we don't anticipate this file to change.
