import fs from 'fs';
import path from 'path';

const src = 'C:\\Users\\Admin\\.gemini\\antigravity\\brain\\7facc79d-47c7-4a6d-9a13-f16ea7355adf\\.user_uploaded\\media_1785841212494.png';
const publicDir = 'C:\\Users\\Admin\\.gemini\\antigravity\\scratch\\windear-landing\\public';

if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir, { recursive: true });
}

fs.copyFileSync(src, path.join(publicDir, 'logo.png'));
fs.copyFileSync(src, path.join(publicDir, 'favicon.png'));
console.log('Logo copied successfully!');
