# A.I.M.A.B.O.T (AI Me Anything Bot)

## Coming Soon currently building 

This app will no longer feature Twilio due to complications of getting a number registered so we will be moving to a web application instead using a htmx frontend and fastapi under the hood :).

## Table of Contents

- [Overview](#overview)
- [Link](#link)
- [Features & Built With](#features--built-with)
- [Usage](#usage)
  - [Opt-In](#opt-in)
  - [Send Questions](#send-questions)
  - [Opt-Out](#opt-out)
- [Issues](#issues)
- [Author](#author)

## Overview

Tired of cluttering your phone with too many apps? Meet **AIMABOT**, your SMS-based assistant that’s just a text away! AIMABOT leverages Twilio's messaging capabilities and OpenAI's ChatGPT to provide quick, concise answers to your everyday questions without the need for lengthy interactions. Seamlessly integrate AIMABOT with Siri for a hands-free experience while driving, or simply use it as a smart assistant through your phone’s messaging app.

Save our Twilio number in your contacts as **AIMABOT** and start enjoying the simplicity of SMS-based assistance!

## Link

[AimaBot](https://aimabot.com)

## Features & Built With

- **Twilio Webhook:** Send and receive SMS messages effortlessly.
  - Built with: [Twilio](https://www.twilio.com/)
- **OpenAI Integration:** Get intelligent responses using ChatGPT 3.5 Turbo.
  - Built with: [OpenAI](https://www.openai.com/)
- **FastAPI:** Benefit from a high-performance web framework for the API.
  - Built with: [FastAPI](https://fastapi.tiangolo.com/)
- **SQLAlchemy and Alembic:** Manage databases and migrations with ease.
  - Built with: [SQLAlchemy](https://www.sqlalchemy.org/), [Alembic](https://alembic.sqlalchemy.org/)
- **AWS ECS Hosting:** Enjoy scalable deployment on AWS infrastructure.
  - Built with: [AWS ECS](https://aws.amazon.com/ecs/)
- **GitHub Actions CI/CD:** Automated linting and deployment checks for smooth development.
  - Built with: [GitHub Actions](https://github.com/features/actions)

## Usage

### Opt-In

Text `START` to our Twilio number to opt in.

### Send Questions

Simply text your questions to the Twilio number, and the ChatGPT assistant will respond promptly.

### Opt-Out

Text `STOP` to our Twilio number to opt out of the service.

## Issues

We are currently working on getting the phone number verified by Twilio. Stay tuned for updates!

## Author

Dhayv

## My Process

I first installed and setup a basic fastapi application. Than I Created the tables and how the were going to be related for my database integrated alembic to migrate the tables. From there it was simply adding the twilio webhooks and openai webhooks testing each webhook indiviually to make sure i was getting the outputs i was seeking. The most difficult part was probaly layering and designing the endpoints since this program had no users and was not receiving information from a frontend and no data was really needed to be validated using pydantic I had to think outside the box from what I am normally used too. I needed to be able to receive data from a users phone to feed to the api which logs the.data into the datbase and and a another endpint is used to essentially read the database to get the users message send it to chatgpt and the response is outputed again via twilio.
