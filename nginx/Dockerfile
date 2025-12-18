FROM nginx:1.25.3-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf

HEALTHCHECK --interval=30s --timeout=5s \
    CMD npx-healthcheck || exit 1 

EXPOSE 80
