import { useRef, useState } from 'react';

export default function ImageUpload({ onFileSelect, disabled }) {
  const inputRef = useRef(null);
  const [preview, setPreview] = useState(null);

  const handleChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setPreview(URL.createObjectURL(file));
    onFileSelect(file);
    // reset so same file can be re-selected
    e.target.value = '';
  };

  const handleClear = () => {
    setPreview(null);
    onFileSelect(null);
  };

  return (
    <div className="flex items-center gap-2">
      {preview ? (
        <div className="relative">
          <img
            src={preview}
            alt="preview"
            className="h-9 w-9 rounded-lg object-cover border border-slate-600"
          />
          <button
            type="button"
            onClick={handleClear}
            className="absolute -top-1.5 -right-1.5 bg-red-500 text-white rounded-full w-4 h-4 flex items-center justify-center text-[10px] leading-none"
          >
            ✕
          </button>
        </div>
      ) : (
        <button
          type="button"
          disabled={disabled}
          onClick={() => inputRef.current?.click()}
          className="p-2 rounded-xl text-slate-400 hover:text-emerald-400 hover:bg-slate-700 transition-colors disabled:opacity-40"
          title="Upload waste image"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </button>
      )}
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={handleChange}
      />
    </div>
  );
}
