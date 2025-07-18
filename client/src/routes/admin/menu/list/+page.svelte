<script>
  import Icon from "@iconify/svelte";
  import { onMount } from "svelte";

  // APIベースURL
  const API_BASE_URL = "http://localhost:8084";

  let menus = [];
  let loading = false;
  let error = null;
  let pagination = {
    page: 1,
    limit: 20,
    total_count: 0,
    total_pages: 0,
    has_next: false,
    has_prev: false,
  };

  // フィルター設定
  let filters = {
    date_from: "",
    date_to: "",
    type: "",
  };

  // 削除処理
  let deletingId = null;
  let deleteConfirm = null;
  let bulkDeleteConfirm = null; // 一括削除確認用

  // 複数選択・一括削除
  let selectedMenus = new Set();
  let selectAll = false;
  let bulkDeleting = false;
  let bulkDeleteMode = "selected"; // "selected" or "filtered"

  // メニュー一覧を取得
  async function fetchMenus(page = 1) {
    loading = true;
    error = null;

    try {
      const params = new URLSearchParams({
        page: page.toString(),
        limit: pagination.limit.toString(),
      });

      // フィルターを追加
      if (filters.date_from) params.append("date_from", filters.date_from);
      if (filters.date_to) params.append("date_to", filters.date_to);
      if (filters.type) params.append("type", filters.type);

      const response = await fetch(`${API_BASE_URL}/admin/menu/list?${params}`);

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      menus = data.menus || [];
      pagination = data.pagination || pagination;
    } catch (err) {
      error = err.message;
      console.error("Failed to fetch menus:", err);
    } finally {
      loading = false;
    }
  }

  // メニュー削除
  async function deleteMenu(menuId) {
    if (deletingId) return; // 削除処理中の場合は無効

    deletingId = menuId;
    try {
      const response = await fetch(
        `${API_BASE_URL}/admin/menu/delete/${menuId}`,
        {
          method: "DELETE",
        },
      );

      const data = await response.json();

      if (response.ok) {
        // 削除成功：リストを再取得
        await fetchMenus(pagination.page);
        deleteConfirm = null;
      } else {
        error = data.error || "削除に失敗しました";
      }
    } catch (err) {
      error = `削除処理中にエラーが発生しました: ${err.message}`;
      console.error("Delete error:", err);
    } finally {
      deletingId = null;
    }
  }

  // 削除確認ダイアログ
  function confirmDelete(menu) {
    deleteConfirm = menu;
  }

  function cancelDelete() {
    deleteConfirm = null;
  }

  // 一括削除確認ダイアログ
  function confirmBulkDelete(mode) {
    bulkDeleteConfirm = { mode };
  }

  function cancelBulkDelete() {
    bulkDeleteConfirm = null;
  }

  // ページ変更
  function changePage(newPage) {
    if (newPage >= 1 && newPage <= pagination.total_pages) {
      fetchMenus(newPage);
    }
  }

  // フィルター適用
  function applyFilters() {
    fetchMenus(1); // フィルター適用時は1ページ目から
  }

  // フィルターリセット
  function resetFilters() {
    filters = {
      date_from: "",
      date_to: "",
      type: "",
    };
    fetchMenus(1);
  }

  // アレルゲン表示用のフォーマット
  function formatAllergens(allergens) {
    if (!allergens || allergens.length === 0) return "なし";
    return allergens.join("、");
  }

  // 日付フォーマット
  function formatDate(dateString) {
    if (!dateString) return "";
    const date = new Date(dateString);
    return date.toLocaleDateString("ja-JP", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    });
  }

  // 複数選択機能
  function toggleSelectAll() {
    if (selectAll) {
      selectedMenus.clear();
    } else {
      menus.forEach((menu) => selectedMenus.add(menu.id));
    }
    selectedMenus = selectedMenus; // リアクティブ更新
    selectAll = !selectAll;
  }

  function toggleSelectMenu(menuId) {
    if (selectedMenus.has(menuId)) {
      selectedMenus.delete(menuId);
    } else {
      selectedMenus.add(menuId);
    }
    selectedMenus = selectedMenus; // リアクティブ更新

    // 全選択状態の更新
    selectAll = selectedMenus.size === menus.length && menus.length > 0;
  }

  // フィルター条件に合致するすべてのレコードを削除
  async function deleteByFilters() {
    if (bulkDeleting) return;

    bulkDeleting = true;
    bulkDeleteMode = "filtered";

    try {
      const response = await fetch(`${API_BASE_URL}/admin/menu/delete/bulk`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          filters: {
            date_from: filters.date_from || undefined,
            date_to: filters.date_to || undefined,
            type: filters.type || undefined,
          },
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // 削除成功：リストを再取得
        await fetchMenus(1); // 1ページ目から再取得
        selectedMenus.clear();
        selectedMenus = selectedMenus;
        selectAll = false;
      } else {
        error = data.error || "一括削除に失敗しました";
      }
    } catch (err) {
      error = `一括削除処理中にエラーが発生しました: ${err.message}`;
      console.error("Bulk delete error:", err);
    } finally {
      bulkDeleting = false;
    }
  }

  // 選択したレコードを削除
  async function deleteSelectedMenus() {
    if (bulkDeleting || selectedMenus.size === 0) return;

    bulkDeleting = true;
    bulkDeleteMode = "selected";

    try {
      const response = await fetch(`${API_BASE_URL}/admin/menu/delete/bulk`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          menu_ids: Array.from(selectedMenus),
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // 削除成功：リストを再取得
        await fetchMenus(pagination.page);
        selectedMenus.clear();
        selectedMenus = selectedMenus;
        selectAll = false;
      } else {
        error = data.error || "選択削除に失敗しました";
      }
    } catch (err) {
      error = `選択削除処理中にエラーが発生しました: ${err.message}`;
      console.error("Selected delete error:", err);
    } finally {
      bulkDeleting = false;
    }
  }

  // フィルターが有効かどうかチェック
  $: hasFilters = filters.date_from || filters.date_to || filters.type;

  // 初期データ読み込み
  onMount(() => {
    fetchMenus();
  });
</script>

<div class="container">
  <h1>日替わりメニュー一覧</h1>

  <!-- フィルター -->
  <div class="filter-section">
    <h2>フィルター</h2>
    <div class="filter-form">
      <div class="filter-group">
        <label for="date-from">開始日:</label>
        <input
          id="date-from"
          type="date"
          bind:value={filters.date_from}
          class="filter-input"
        />
      </div>

      <div class="filter-group">
        <label for="date-to">終了日:</label>
        <input
          id="date-to"
          type="date"
          bind:value={filters.date_to}
          class="filter-input"
        />
      </div>

      <div class="filter-group">
        <label for="type-filter">メニュータイプ:</label>
        <select id="type-filter" bind:value={filters.type} class="filter-input">
          <option value="">すべて</option>
          <option value="A">Aセット</option>
          <option value="B">Bセット</option>
        </select>
      </div>

      <div class="filter-buttons">
        <button class="apply-button" on:click={applyFilters}>
          <Icon icon="ph:magnifying-glass" width="16" />
          フィルター適用
        </button>
        <button class="reset-button" on:click={resetFilters}>
          <Icon icon="ph:x" width="16" />
          リセット
        </button>

        <!-- フィルター条件に合致するすべてのレコードを削除 -->
        {#if hasFilters}
          <button
            class="bulk-delete-button filter-delete"
            on:click={() => confirmBulkDelete("filtered")}
            disabled={bulkDeleting}
          >
            {#if bulkDeleting && bulkDeleteMode === "filtered"}
              <Icon icon="ph:spinner" width="16" class="spinning" />
              削除中...
            {:else}
              <Icon icon="ph:trash" width="16" />
              フィルター条件で削除
            {/if}
          </button>
        {/if}
      </div>
    </div>
  </div>

  <!-- メニューテーブル -->
  <div class="table-section">
    {#if loading}
      <div class="loading">
        <Icon icon="ph:spinner" width="32" class="spinning" />
        <p>メニューを読み込み中...</p>
      </div>
    {:else if error}
      <div class="error">
        <Icon icon="ph:warning" width="24" />
        <p>エラー: {error}</p>
        <button
          class="retry-button"
          on:click={() => fetchMenus(pagination.page)}
        >
          <Icon icon="ph:arrow-clockwise" width="16" />
          再試行
        </button>
      </div>
    {:else if menus.length === 0}
      <div class="empty">
        <Icon icon="ph:empty" width="48" />
        <p>メニューが見つかりません</p>
      </div>
    {:else}
      <!-- 選択削除コントロール -->
      {#if selectedMenus.size > 0}
        <div class="selection-controls">
          <div class="selection-info">
            <Icon icon="ph:check-square" width="20" />
            <span>{selectedMenus.size}件選択中</span>
          </div>
          <button
            class="bulk-delete-button selected-delete"
            on:click={() => confirmBulkDelete("selected")}
            disabled={bulkDeleting}
          >
            {#if bulkDeleting && bulkDeleteMode === "selected"}
              <Icon icon="ph:spinner" width="16" class="spinning" />
              削除中...
            {:else}
              <Icon icon="ph:trash" width="16" />
              選択した項目を削除
            {/if}
          </button>
        </div>
      {/if}

      <div class="table-container">
        <table class="menu-table">
          <thead>
            <tr>
              <th class="checkbox-column">
                <input
                  type="checkbox"
                  bind:checked={selectAll}
                  on:change={toggleSelectAll}
                  class="select-checkbox"
                />
              </th>
              <th>日付</th>
              <th>タイプ</th>
              <th>メニュー名</th>
              <th>価格</th>
              <th>エネルギー</th>
              <th>アレルゲン</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {#each menus as menu}
              <tr class:selected={selectedMenus.has(menu.id)}>
                <td class="checkbox-column">
                  <input
                    type="checkbox"
                    checked={selectedMenus.has(menu.id)}
                    on:change={() => toggleSelectMenu(menu.id)}
                    class="select-checkbox"
                  />
                </td>
                <td>{formatDate(menu.date)}</td>
                <td>
                  <span class="type-badge type-{menu.type.toLowerCase()}">
                    {menu.type}セット
                  </span>
                </td>
                <td class="menu-name">{menu.name}</td>
                <td class="price">¥{menu.price}</td>
                <td>{menu.energy}kcal</td>
                <td class="allergens">{formatAllergens(menu.allergens)}</td>
                <td>
                  <button
                    class="delete-button"
                    on:click={() => confirmDelete(menu)}
                    disabled={deletingId === menu.id}
                    title="削除"
                  >
                    {#if deletingId === menu.id}
                      <Icon icon="ph:spinner" width="16" class="spinning" />
                    {:else}
                      <Icon icon="ph:trash" width="16" />
                    {/if}
                  </button>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>

      <!-- ページネーション -->
      <div class="pagination">
        <div class="pagination-info">
          <p>
            {pagination.total_count}件中
            {Math.min(
              (pagination.page - 1) * pagination.limit + 1,
              pagination.total_count,
            )}〜{Math.min(
              pagination.page * pagination.limit,
              pagination.total_count,
            )}件を表示
          </p>
        </div>

        <div class="pagination-controls">
          <button
            class="page-button"
            on:click={() => changePage(pagination.page - 1)}
            disabled={!pagination.has_prev || loading}
          >
            <Icon icon="ph:caret-left" width="16" />
            前へ
          </button>

          <span class="page-info">
            {pagination.page} / {pagination.total_pages}
          </span>

          <button
            class="page-button"
            on:click={() => changePage(pagination.page + 1)}
            disabled={!pagination.has_next || loading}
          >
            次へ
            <Icon icon="ph:caret-right" width="16" />
          </button>
        </div>
      </div>
    {/if}
  </div>
</div>

<!-- 削除確認モーダル -->
{#if deleteConfirm}
  <div class="modal-overlay" on:click={cancelDelete}>
    <div class="modal" on:click|stopPropagation>
      <h3>メニュー削除の確認</h3>
      <div class="confirm-content">
        <p><strong>以下のメニューを削除してもよろしいですか？</strong></p>
        <div class="menu-info">
          <p><strong>日付:</strong> {formatDate(deleteConfirm.date)}</p>
          <p><strong>タイプ:</strong> {deleteConfirm.type}セット</p>
          <p><strong>メニュー名:</strong> {deleteConfirm.name}</p>
          <p><strong>ID:</strong> {deleteConfirm.id}</p>
        </div>
        <p class="warning">この操作は取り消すことができません。</p>
      </div>
      <div class="modal-buttons">
        <button class="cancel-button" on:click={cancelDelete}>
          <Icon icon="ph:x" width="16" />
          キャンセル
        </button>
        <button
          class="confirm-delete-button"
          on:click={() => deleteMenu(deleteConfirm.id)}
          disabled={deletingId}
        >
          {#if deletingId}
            <Icon icon="ph:spinner" width="16" class="spinning" />
            削除中...
          {:else}
            <Icon icon="ph:trash" width="16" />
            削除する
          {/if}
        </button>
      </div>
    </div>
  </div>
{/if}

<!-- 一括削除確認モーダル -->
{#if bulkDeleteConfirm}
  <div class="modal-overlay" on:click={cancelBulkDelete}>
    <div class="modal" on:click|stopPropagation>
      <h3>一括削除の確認</h3>
      <div class="confirm-content">
        {#if bulkDeleteConfirm.mode === "filtered"}
          <p>
            <strong
              >フィルター条件に合致するすべてのメニューを削除してもよろしいですか？</strong
            >
          </p>
          <div class="menu-info">
            <p><strong>削除対象:</strong></p>
            <ul>
              {#if filters.date_from}<li>
                  開始日: {formatDate(filters.date_from)}
                </li>{/if}
              {#if filters.date_to}<li>
                  終了日: {formatDate(filters.date_to)}
                </li>{/if}
              {#if filters.type}<li>
                  メニュータイプ: {filters.type}セット
                </li>{/if}
            </ul>
            <p>
              <strong>注意:</strong> 現在のページに表示されているメニューだけでなく、フィルター条件に合致するすべてのメニューが削除されます。
            </p>
          </div>
        {:else if bulkDeleteConfirm.mode === "selected"}
          <p>
            <strong
              >選択した {selectedMenus.size} 件のメニューを削除してもよろしいですか？</strong
            >
          </p>
          <div class="menu-info">
            <p><strong>削除対象メニューID:</strong></p>
            <p class="selected-ids">{Array.from(selectedMenus).join(", ")}</p>
          </div>
        {/if}
        <p class="warning">この操作は取り消すことができません。</p>
      </div>
      <div class="modal-buttons">
        <button class="cancel-button" on:click={cancelBulkDelete}>
          <Icon icon="ph:x" width="16" />
          キャンセル
        </button>
        <button
          class="confirm-delete-button"
          on:click={() => {
            if (bulkDeleteConfirm.mode === "filtered") {
              deleteByFilters();
            } else {
              deleteSelectedMenus();
            }
            bulkDeleteConfirm = null;
          }}
          disabled={bulkDeleting}
        >
          {#if bulkDeleting}
            <Icon icon="ph:spinner" width="16" class="spinning" />
            削除中...
          {:else}
            <Icon icon="ph:trash" width="16" />
            削除する
          {/if}
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .container {
    padding: 0;
  }

  h1 {
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 1.5rem;
    color: #333;
  }

  h2 {
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 1rem;
    color: #444;
  }

  /* フィルターセクション */
  .filter-section {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    border: 1px solid #e9ecef;
  }

  .filter-form {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    align-items: end;
  }

  .filter-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .filter-group label {
    font-weight: 500;
    color: #555;
    font-size: 0.9rem;
  }

  .filter-input {
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 0.9rem;
  }

  .filter-buttons {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .apply-button,
  .reset-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: background-color 0.2s;
  }

  .apply-button {
    background: #007bff;
    color: white;
  }

  .apply-button:hover {
    background: #0056b3;
  }

  .reset-button {
    background: #6c757d;
    color: white;
  }

  .reset-button:hover {
    background: #545b62;
  }

  /* 一括削除ボタン */
  .bulk-delete-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: background-color 0.2s;
  }

  .bulk-delete-button.filter-delete {
    background: #dc3545;
    color: white;
  }

  .bulk-delete-button.filter-delete:hover:not(:disabled) {
    background: #c82333;
  }

  .bulk-delete-button.selected-delete {
    background: #dc3545;
    color: white;
  }

  .bulk-delete-button.selected-delete:hover:not(:disabled) {
    background: #c82333;
  }

  .bulk-delete-button:disabled {
    background: #6c757d;
    cursor: not-allowed;
  }

  /* 選択コントロール */
  .selection-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    background: #e3f2fd;
    border-bottom: 1px solid #e9ecef;
  }

  .selection-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
    color: #1976d2;
  }

  /* チェックボックス */
  .checkbox-column {
    width: 40px;
    text-align: center;
  }

  .select-checkbox {
    width: 16px;
    height: 16px;
    cursor: pointer;
  }

  .menu-table tbody tr.selected {
    background: #e3f2fd;
  }

  .menu-table tbody tr.selected:hover {
    background: #bbdefb;
  }

  /* テーブルセクション */
  .table-section {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }

  .table-container {
    overflow-x: auto;
  }

  .menu-table {
    width: 100%;
    border-collapse: collapse;
  }

  .menu-table th,
  .menu-table td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid #e9ecef;
  }

  .menu-table th {
    background: #f8f9fa;
    font-weight: 600;
    color: #495057;
    position: sticky;
    top: 0;
    z-index: 1;
  }

  .menu-table tbody tr:hover {
    background: #f8f9fa;
  }

  .type-badge {
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
  }

  .type-a {
    background: #e3f2fd;
    color: #1976d2;
  }

  .type-b {
    background: #f3e5f5;
    color: #7b1fa2;
  }

  .menu-name {
    font-weight: 500;
    max-width: 200px;
    word-wrap: break-word;
  }

  .price {
    font-weight: 600;
    color: #d32f2f;
  }

  .allergens {
    font-size: 0.85rem;
    color: #666;
    max-width: 150px;
    word-wrap: break-word;
  }

  .delete-button {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem;
    background: #dc3545;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .delete-button:hover:not(:disabled) {
    background: #c82333;
  }

  .delete-button:disabled {
    background: #6c757d;
    cursor: not-allowed;
  }

  /* ページネーション */
  .pagination {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    background: #f8f9fa;
    border-top: 1px solid #e9ecef;
  }

  .pagination-info p {
    margin: 0;
    font-size: 0.9rem;
    color: #6c757d;
  }

  .pagination-controls {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .page-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background-color 0.2s;
  }

  .page-button:hover:not(:disabled) {
    background: #0056b3;
  }

  .page-button:disabled {
    background: #6c757d;
    cursor: not-allowed;
  }

  .page-info {
    font-weight: 500;
    color: #495057;
  }

  /* ステータス表示 */
  .loading,
  .error,
  .empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    text-align: center;
  }

  .loading {
    color: #6c757d;
  }

  .error {
    color: #dc3545;
  }

  .empty {
    color: #6c757d;
  }

  .retry-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background: #dc3545;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
  }

  .retry-button:hover {
    background: #c82333;
  }

  /* モーダル */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    max-width: 500px;
    width: 90%;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  }

  .modal h3 {
    margin: 0 0 1rem 0;
    color: #333;
  }

  .confirm-content {
    margin: 1rem 0;
  }

  .menu-info {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 6px;
    margin: 1rem 0;
  }

  .menu-info p {
    margin: 0.25rem 0;
    font-size: 0.9rem;
  }

  .warning {
    color: #dc3545;
    font-weight: 500;
    font-size: 0.9rem;
  }

  .modal-buttons {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    margin-top: 1.5rem;
  }

  .cancel-button,
  .confirm-delete-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: background-color 0.2s;
  }

  .cancel-button {
    background: #6c757d;
    color: white;
  }

  .cancel-button:hover {
    background: #545b62;
  }

  .confirm-delete-button {
    background: #dc3545;
    color: white;
  }

  .confirm-delete-button:hover:not(:disabled) {
    background: #c82333;
  }

  .confirm-delete-button:disabled {
    background: #6c757d;
    cursor: not-allowed;
  }

  /* 一括削除確認モーダル用スタイル */
  .menu-info ul {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
  }

  .menu-info li {
    margin: 0.25rem 0;
    font-size: 0.9rem;
  }

  .selected-ids {
    font-family: monospace;
    font-size: 0.8rem;
    word-break: break-all;
    background: #f1f3f4;
    padding: 0.5rem;
    border-radius: 4px;
    max-height: 100px;
    overflow-y: auto;
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

  /* レスポンシブ */
  @media (max-width: 768px) {
    .container {
      padding: 0.5rem;
    }

    .filter-form {
      grid-template-columns: 1fr;
    }

    .pagination {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }

    .menu-table {
      font-size: 0.85rem;
    }

    .menu-table th,
    .menu-table td {
      padding: 0.5rem;
    }
  }
</style>
