import React, { useState } from 'react';
import UploadLanding from './components/UploadLanding';
import Workspace from './components/Workspace';

function App() {
  const [fileData, setFileData] = useState(null);

  if (!fileData) {
    return <UploadLanding onUploadSuccess={setFileData} />;
  }

  return (
    <Workspace
      fileData={fileData}
      onBack={() => setFileData(null)}
    />
  );
}

export default App;
