# Goal

Create a script which can create and execute a financial action plan.

Main variables to build this plan are current Net Worth and Spending.

Action plan should execute and update net worth until the value reaches a given `GOAL_DOLLARS`

## Step 1

hardcoded variables and simple dictionaries to address my curiosity.

> note: values used and saved to Git are either targeting averages in florida or spitballed

## Step 2

fastapi + jinja html templates to collect user info

## Possible Extensions

Incorporate the action plan logic into an API or Lambda and build a frontend.

Include logic to provide an alternative action plan to become debt-free.

# Dev Notes
to run the server locally, you can either run the app.py file, or use this cli command:
`uvicorn app:app --reload --reload-include \*.html`

to use any new tailwind classes, you will also need to run tailwind:
`tailwindcss -i ./app/static/src/tw.css -o ./app/static/css/main.css --watch`