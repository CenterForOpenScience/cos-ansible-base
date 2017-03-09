#!/usr/bin/env node
var prerender = require('./lib');

var server = prerender({
    workers: process.env.PRERENDER_NUM_WORKERS || 1,
    iterations: process.env.PRERENDER_NUM_ITERATIONS || 40,
    softIterations: process.env.PRERENDER_NUM_SOFT_ITERATIONS || 30
});


server.use(prerender.sendPrerenderHeader());
// server.use(prerender.basicAuth());
server.use(prerender.whitelist());
// server.use(prerender.blacklist());
// server.use(prerender.logger());
server.use(prerender.removeScriptTags());
server.use(prerender.httpHeaders());

// Cache
// server.use(require('prerender-redis-cache'));
server.use(prerender.inMemoryHtmlCache());
// server.use(prerender.s3HtmlCache());

// Throttling header
// server.use({
//     onPhantomPageCreate: function(phantom, req, res, next) {
//         req.prerender.page.run(function(resolve) {
//             var customHeaders = this.customHeaders;
//             customHeaders['X-THROTTLE-TOKEN'] = 'CHANGEME';
//             this.customHeaders = customHeaders;
//             resolve();
//         }).then(function() {
//             next();
//         }).catch(function() {
//             next();
//         });
//         }
// });

server.start();
