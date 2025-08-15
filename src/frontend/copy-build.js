const fs = require('fs-extra');
const path = require('path');

async function copyBuildFiles() {
  try {
    const source = path.resolve(__dirname, 'dist');
    const destination = path.resolve(__dirname, '../backend/static');
    
    // Ensure destination directory exists
    await fs.ensureDir(destination);
    
    // Copy all files from build to static directory
    await fs.copy(source, destination);
    
    console.log('Build files copied to static directory successfully!');
  } catch (error) {
    console.error('Error copying build files:', error);
  }
}

copyBuildFiles();