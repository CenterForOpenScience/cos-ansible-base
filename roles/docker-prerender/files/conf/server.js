var prerender = require('prerender');

var server = prerender({
        workers: 2,
        iterations: 10,
        phantomBasePort: 12300,
        messageTimeout: process.env.PHANTOM_CLUSTER_MESSAGE_TIMEOUT
});

server.use(prerender.whitelist());
server.use(prerender.removeScriptTags());
server.use(prerender.httpHeaders());
server.use(prerender.inMemoryHtmlCache());

server.start();
