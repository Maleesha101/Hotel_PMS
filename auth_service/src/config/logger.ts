import winston from 'winston';

const { combine, timestamp, json, errors, printf } = winston.format;

const logger = winston.createLogger({
  level: 'info',
  format: combine(
    timestamp(),
    errors({ stack: true }),
    json()
  ),
  transports: [new winston.transports.Console()],
});

export { logger };
