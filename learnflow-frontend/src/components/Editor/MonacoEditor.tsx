'use client';

import Editor from '@monaco-editor/react';
import { useState } from 'react';

interface MonacoEditorProps {
  onChange: (code: string) => void;
  onSubmit: (code: string) => void;
}

export default function MonacoEditor({ onChange, onSubmit }: MonacoEditorProps) {
  const [code, setCode] = useState('// Write Python code here\\n');

  return (
    <Editor
      height="70vh"
      language="python"
      theme="vs-dark"
      value={code}
      onChange={(value) => {
        setCode(value || '');
        onChange(value || '');
      }}
      options={{
        minimap: { enabled: false },
        fontSize: 14,
        wordWrap: 'on',
      }}
      onMount={(editor) => {
        editor.addAction({
          id: 'submit-code',
          label: 'Submit Code',
          keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter],
          run: () => onSubmit(code),
        });
      }}
    />
  );
}
