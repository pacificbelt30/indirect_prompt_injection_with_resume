const pdfForm = document.getElementById('pdf-form');
const pdfFile = document.getElementById('pdf-file');
const summaryField = document.getElementById('summary');
const evaluationField = document.getElementById('evaluation');
const uploadButton = document.getElementById('upload');

uploadButton.addEventListener('click', async (event) => {
  pdfForm.dispatchEvent(new Event('submit')); // アップロード処理をトリガー
});

pdfForm.addEventListener('submit', async (event) => {
  event.preventDefault(); // ページのリロードを防ぐ

  // ローディング中の表示を開始
  const loadingMessage = document.createElement('p');
  loadingMessage.textContent = '処理中...';
  loadingMessage.id = 'loading-message';
  result.appendChild(loadingMessage);

  const formData = new FormData();
  formData.append('pdf', pdfFile.files[0]);

  try {
    const response = await fetch('http://localhost:8000/api/analyze_pdf', { // APIエンドポイントに調整
      method: 'POST',
      body: formData
    });

    // タイムアウト処理 (例: 5秒)
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('Timeout')), 5000);
    });

    const result = await Promise.race([response.json(), timeoutPromise]);

    summaryField.textContent = result.result || '要約を取得できませんでした。';
    evaluationField.textContent = result.evaluation || '総評を取得できませんでした。';

  } catch (error) {
    summaryField.textContent = 'エラーが発生しました。';
    evaluationField.textContent = error.message;
  }


  // ... (PDF送信、レスポンス処理) ...

  // ローディング中の表示を終了
  result.removeChild(loadingMessage); 
});



// ドラッグ＆ドロップの処理を追加
const dropArea = document.getElementById('pdf-form');

['dragover', 'dragenter'].forEach(eventName => {
  dropArea.addEventListener(eventName, preventDefaults, false);
});

['dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, (e) => {
    preventDefaults(e);
    dropArea.classList.remove('is-dragover');
  }, false);
});

dropArea.addEventListener('drop', handleDrop, false);

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
  dropArea.classList.add('is-dragover');
}

function handleDrop(e) {
  const dt = e.dataTransfer;
  const files = dt.files;

  if (files.length > 0) {
    pdfFile.files = files;
    pdfForm.dispatchEvent(new Event('submit')); // アップロード処理をトリガー
  }
}
