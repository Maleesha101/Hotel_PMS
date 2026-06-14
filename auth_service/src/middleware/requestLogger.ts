import morgan, { StreamOptions } from 'morgan';
import { logger } from '../config/logger';

// Define a stream that writes to winston
const stream: StreamOptions = {
  write: (message) => logger.info(message.trim()),
};

// Use combined format for detailed logs
export const requestLogger = morgan('combined', { stream });
