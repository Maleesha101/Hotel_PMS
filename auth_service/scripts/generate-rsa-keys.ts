import { generateKeyPairSync } from 'crypto';
import * as fs from 'fs';
import * as path from 'path';

const { privateKey, publicKey } = generateKeyPairSync('rsa', {
  modulusLength: 2048,
  publicKeyEncoding: { type: 'spki', format: 'pem' },
  privateKeyEncoding: { type: 'pkcs8', format: 'pem' },
});

const keysDir = path.join(__dirname, '..', '.keys');
if (!fs.existsSync(keysDir)) {
  fs.mkdirSync(keysDir);
}
fs.writeFileSync(path.join(keysDir, 'private.pem'), privateKey);
fs.writeFileSync(path.join(keysDir, 'public.pem'), publicKey);

// Automatically update or create .env file
const envPath = path.join(__dirname, '..', '.env');
const privateKeyEscaped = privateKey.replace(/\n/g, '\\n');
const publicKeyEscaped = publicKey.replace(/\n/g, '\\n');

let envContent = fs.existsSync(envPath) ? fs.readFileSync(envPath, 'utf8') : '';

const updateOrAdd = (content: string, key: string, value: string) => {
  const regex = new RegExp(`^${key}=.*`, 'm');
  const newLine = `${key}="${value}"`;
  return content.match(regex) ? content.replace(regex, newLine) : content + (content.endsWith('\n') || content === '' ? '' : '\n') + newLine + '\n';
};

envContent = updateOrAdd(envContent, 'JWT_PRIVATE_KEY', privateKeyEscaped);
envContent = updateOrAdd(envContent, 'JWT_PUBLIC_KEY', publicKeyEscaped);

fs.writeFileSync(envPath, envContent.trim() + '\n');

console.log('RS256 key pair generated at .keys/');
console.log('Keys automatically added to your .env file');
console.log('\n--- PRIVATE KEY (set as JWT_PRIVATE_KEY env var) ---');
console.log(privateKey);
console.log('\n--- PUBLIC KEY (set as JWT_PUBLIC_KEY env var) ---');
console.log(publicKey);
