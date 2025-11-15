FROM python:3.13.7-alpine

# Generic labels
LABEL maintainer="Marco Corbetta <corbettamarco.it@gmail.com>"
LABEL version="0.1"
LABEL description="My own custom 12ft.io replacement"
LABEL url="https://github.com/corbettamarco/13ft"
LABEL documentation="https://github.com/corbettamarco/13ft/blob/master/README.md"

# OCI compliant labels
LABEL org.opencontainers.image.source="https://github.com/corbettamarco/13ft"
LABEL org.opencontainers.image.authors="Marco Corbetta"
LABEL org.opencontainers.image.created="2023-10-31T22:53:00Z"
LABEL org.opencontainers.image.version="0.1"
LABEL org.opencontainers.image.url="https://github.com/corbettamarco/13ft/"
LABEL org.opencontainers.image.source="https://github.com/corbettamarco/13ft/"
LABEL org.opencontainers.image.description="My own custom 12ft.io replacement"
LABEL org.opencontainers.image.documentation="https://github.com/corbettamarco/13ft/blob/master/README.md"
LABEL org.opencontainers.image.licenses=MIT

COPY . .
RUN pip install -r requirements.txt
WORKDIR /app
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "portable.py" ] 