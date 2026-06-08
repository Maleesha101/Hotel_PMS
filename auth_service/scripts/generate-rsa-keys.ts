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

console.log('✅ RS256 key pair generated at .keys/');
console.log('\n--- PRIVATE KEY (set as JWT_PRIVATE_KEY env var) ---');
console.log(privateKey);
console.log('\n--- PUBLIC KEY (set as JWT_PUBLIC_KEY env var) ---');
console.log(publicKey);
