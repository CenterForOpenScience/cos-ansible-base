server {
        listen 80;
        server_name sentry2.osf.io;

        rewrite ^ https://$server_name$request_uri? permanent;
}

server {
        listen 443;
        server_name sentry2.osf.io;

        ssl on;
        ssl_certificate /etc/ssl/private/default.crt;
        ssl_certificate_key /etc/ssl/private/default.key;
        ssl_session_timeout 5m;
        ssl_protocols SSLv3 TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers "HIGH:!aNULL:!MD5 or HIGH:!aNULL:!MD5:!3DES";
        ssl_prefer_server_ciphers on;

        client_max_body_size 20M;

        location / {
                proxy_pass      http://sentry:9000;
                proxy_redirect  off;
                proxy_set_header        Host                    $host;
                proxy_set_header        X-Real-IP               $remote_addr;
                proxy_set_header        X-Forwarded-For         $proxy_add_x_forwarded_for;
                proxy_set_header        X-Forwarded-Proto       $scheme;
        }
}