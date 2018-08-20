FROM nginx

RUN rm /etc/nginx/nginx.conf
ADD nginx.conf /etc/nginx/

RUN rm /etc/nginx/conf.d/default.conf
ADD steemy.conf /etc/nginx/conf.d/

RUN rm /etc/nginx/mime.types
ADD mime.types /etc/nginx/


