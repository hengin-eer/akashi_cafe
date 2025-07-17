<script>
  import Icon from "@iconify/svelte";

  // APIベースURL
  const API_BASE_URL = "http://localhost:8084";

  let file = null;
  let uploading = false;
  let uploadResult = null;
  let error = null;

  // ファイル選択時の処理
  function handleFileSelect(event) {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      file = selectedFile;
      uploadResult = null;
      error = null;
    }
  }

  // ファイルアップロード処理
  async function uploadFile() {
    if (!file) {
      error = "ファイルを選択してください";
      return;
    }

    if (!file.name.toLowerCase().endsWith(".csv")) {
      error = "CSVファイルのみアップロード可能です";
      return;
    }

    uploading = true;
    error = null;
    uploadResult = null;

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_BASE_URL}/admin/menu/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        uploadResult = data;
        file = null;
        // ファイル入力をリセット
        const fileInput = document.getElementById("csv-file");
        if (fileInput) fileInput.value = "";
      } else {
        error = data.error || "アップロードに失敗しました";
      }
    } catch (err) {
      error = `ネットワークエラーが発生しました: ${err.message}`;
      console.error("Upload error:", err);
    } finally {
      uploading = false;
    }
  }

  // ファイルサイズを人間が読みやすい形式に変換
  function formatFileSize(bytes) {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  }

  // 結果をリセット
  function resetForm() {
    file = null;
    uploadResult = null;
    error = null;
    const fileInput = document.getElementById("csv-file");
    if (fileInput) fileInput.value = "";
  }
</script>

<div class="container">
  <h1>日替わりメニュー追加</h1>

  <div class="upload-section">
    <h2>ファイルアップロード</h2>

    <div class="file-input-container">
      <label for="csv-file" class="file-label">
        <Icon icon="ph:file-csv" width="24" />
        CSVファイルを選択
      </label>
      <input
        id="csv-file"
        type="file"
        accept=".csv"
        on:change={handleFileSelect}
        class="file-input"
      />
    </div>

    {#if file}
      <div class="file-info">
        <div class="file-details">
          <Icon icon="ph:file-csv" width="20" />
          <span class="filename">{file.name}</span>
          <span class="filesize">({formatFileSize(file.size)})</span>
        </div>
      </div>
    {/if}

    <div class="upload-controls">
      <button
        class="upload-button"
        on:click={uploadFile}
        disabled={!file || uploading}
      >
        {#if uploading}
          <Icon icon="ph:spinner" width="20" class="spinning" />
          アップロード中...
        {:else}
          <Icon icon="ph:upload" width="20" />
          アップロード
        {/if}
      </button>

      {#if file || uploadResult || error}
        <button class="reset-button" on:click={resetForm}>
          <Icon icon="ph:x" width="20" />
          リセット
        </button>
      {/if}
    </div>
  </div>

  <!-- 結果表示 -->
  {#if error}
    <div class="result error">
      <div class="result-header">
        <Icon icon="ph:x-circle" width="24" />
        <h3>エラー</h3>
      </div>
      <p>{error}</p>
      {#if uploadResult?.errors}
        <div class="error-details">
          <h4>詳細エラー:</h4>
          <ul>
            {#each uploadResult.errors as err}
              <li>{err}</li>
            {/each}
          </ul>
        </div>
      {/if}
    </div>
  {/if}

  {#if uploadResult && !error}
    <div class="result success">
      <div class="result-header">
        <Icon icon="ph:check-circle" width="24" />
        <h3>アップロード完了</h3>
      </div>
      <p>{uploadResult.message}</p>
      <div class="result-stats">
        <div class="stat">
          <span class="stat-label">追加件数:</span>
          <span class="stat-value">{uploadResult.inserted_count}件</span>
        </div>
      </div>

      {#if uploadResult.errors && uploadResult.errors.length > 0}
        <div class="warning-details">
          <h4>警告 (一部データでエラーが発生しました):</h4>
          <ul>
            {#each uploadResult.errors as err}
              <li>{err}</li>
            {/each}
          </ul>
        </div>
      {/if}
    </div>
  {/if}

  <div class="info-section">
    <h2>アップロード方法</h2>
    <p>CSVファイルを選択してアップロードボタンを押してください。</p>

    <div class="format-info">
      <h3>CSVファイルの形式</h3>
      <p><strong>必須カラム:</strong></p>
      <div class="columns">
        <code
          >id, date, type, name, price, energy, protein, fat, carb, salt,
          allergens</code
        >
      </div>

      <h4>例:</h4>
      <div class="example">
        <code>
          D-9001,2025-08-01,A,鶏の照り焼き,430,650,25.5,18.2,95.8,3.2,"小麦,そば"
        </code>
      </div>

      <div class="constraints">
        <h4>制約:</h4>
        <ul>
          <li>日付: YYYY-MM-DD 形式</li>
          <li>メニュータイプ: A または B</li>
          <li>価格・エネルギー: 整数</li>
          <li>栄養成分: 小数点可能</li>
          <li>アレルゲン: 小麦,卵,乳,そば,落花生,えび,かに,くるみ</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<style>
  .container {
    max-width: 800px;
    margin: auto;
    padding: 0;
  }

  h1 {
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 1rem;
    color: #333;
  }

  h2 {
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 0.75rem;
    color: #444;
  }

  h3 {
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
    color: #555;
  }

  h4 {
    font-size: 1rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
    color: #666;
  }

  .info-section {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    border: 1px solid #e9ecef;
  }

  .format-info {
    margin-top: 1rem;
  }

  .columns {
    background: #fff;
    padding: 0.75rem;
    border-radius: 6px;
    border: 1px solid #dee2e6;
    margin: 0.5rem 0;
    font-family: monospace;
    font-size: 0.9rem;
    overflow-x: auto;
  }

  .example {
    background: #fff;
    padding: 0.75rem;
    border-radius: 6px;
    border: 1px solid #dee2e6;
    margin: 0.5rem 0;
    font-family: monospace;
    font-size: 0.85rem;
    overflow-x: auto;
  }

  .constraints ul {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
  }

  .constraints li {
    margin-bottom: 0.25rem;
    font-size: 0.9rem;
  }

  .upload-section {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 2rem;
  }

  .file-input-container {
    margin-bottom: 1rem;
  }

  .file-label {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: #e9ecef;
    border: 2px dashed #adb5bd;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
  }

  .file-label:hover {
    background: #dee2e6;
    border-color: #6c757d;
  }

  .file-input {
    display: none;
  }

  .file-info {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    border: 1px solid #e9ecef;
  }

  .file-details {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .filename {
    font-weight: 500;
    color: #495057;
  }

  .filesize {
    color: #6c757d;
    font-size: 0.9rem;
  }

  .upload-controls {
    display: flex;
    gap: 1rem;
    align-items: center;
  }

  .upload-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
    transition: background-color 0.2s;
  }

  .upload-button:hover:not(:disabled) {
    background: #0056b3;
  }

  .upload-button:disabled {
    background: #6c757d;
    cursor: not-allowed;
  }

  .reset-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: #6c757d;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
    transition: background-color 0.2s;
  }

  .reset-button:hover {
    background: #545b62;
  }

  .result {
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 1rem;
  }

  .result.success {
    background: #d1edff;
    border: 1px solid #0c5460;
    color: #0c5460;
  }

  .result.error {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
  }

  .result-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .result-header h3 {
    margin: 0;
  }

  .result-stats {
    display: flex;
    gap: 1rem;
    margin: 1rem 0;
  }

  .stat {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .stat-label {
    font-size: 0.9rem;
    font-weight: 500;
  }

  .stat-value {
    font-size: 1.1rem;
    font-weight: bold;
  }

  .error-details,
  .warning-details {
    margin-top: 1rem;
  }

  .error-details ul,
  .warning-details ul {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
  }

  .error-details li,
  .warning-details li {
    margin-bottom: 0.25rem;
    font-size: 0.9rem;
  }

  .spinning {
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }

  @media (max-width: 600px) {
    .container {
      padding: 0.5rem;
    }

    .upload-controls {
      flex-direction: column;
      align-items: stretch;
    }

    .upload-button,
    .reset-button {
      justify-content: center;
    }
  }
</style>
