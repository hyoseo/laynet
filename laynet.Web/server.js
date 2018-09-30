const http = require('http');
const path = require('path');
const createError = require('http-errors');
const express = require('express');
const logger = require('morgan');

const indexRouter = require('./routes/index');
const stockRouter = require('./routes/stock');

const app = express();

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.use(logger('dev'));
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/stock', stockRouter);

app.use((req, res, next) => {
    next(createError(404));
});

app.use((err, req, res, next) => {
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    res.status(err.status || 500);
    res.render('error');
});

const server = http.createServer(app);
const port = 8080;

server.listen(port);
server.on('error', onError);
server.on('listening', onListening);

function onError(error) {
    if (error.syscall !== 'listen') {
        throw error;
    }

    switch (error.code) {
        case 'EACCES':
            console.error(`Port ${port} requires elevated privileges`);
            process.exit(1);
            break;
        case 'EADDRINUSE':
            console.error(`Port ${port} is already in use`);
            process.exit(1);
            break;
        default:
            throw error;
    }
}

function onListening() {
    console.log(`Listening on ${port}`);
}

/*
db.getLatestStockTrade('251270').then(result => {
    console.log(result);
});

db.getStockTradeAfterTheDate('251270', date.getDateDaysAgo(14)).then(result => {
    console.log(result);
});

db.getBigPlayersDataAfterTheDate('251270', date.getDateMonthsAgo(1)).then(result => {
    console.log(result);
});
*/