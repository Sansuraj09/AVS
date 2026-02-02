// Shim entrypoint so `node server.js` works in both CommonJS and ESM modes.
// It delegates to the actual server implementation in server_visitor.js
// Support both ESM (when parent package.json has "type":"module")
// and CommonJS environments.
try {
    // If `require` is available (CommonJS), use it directly.
        if (typeof require === 'function') {
            require('./server_visitor.cjs');
        } else {
        // In ESM, create a require function to load the CommonJS server file.
        import('module').then(({ createRequire }) => {
            const requireC = createRequire(import.meta.url);
            requireC('./server_visitor.cjs');
        }).catch(err => {
            console.error('Failed to start server from server_visitor.cjs:', err);
            process.exit(1);
        });
    }
} catch (err) {
    console.error('Failed to start server from server_visitor.js:', err);
    process.exit(1);
}
