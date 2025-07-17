<script>
  import Icon from "@iconify/svelte";
  import { onMount } from "svelte";

  // APIベースURL
  const API_BASE_URL = "http://localhost:8084";

  let menus = [];
  let loading = false;
  let error = null;
  let selectedDate = "";

  // 今日の日付を取得
  const today = new Date();
  const todayString = today.toISOString().split("T")[0];

  // 日付選択の初期値を今日に設定
  selectedDate = todayString;

  // メニュー取得
  async function fetchMenus() {
    if (!selectedDate) return;

    loading = true;
    error = null;

    try {
      const response = await fetch(
        `${API_BASE_URL}/menu/list?date=${selectedDate}`,
      );

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      menus = data.menus || [];
    } catch (err) {
      error = err.message;
      console.error("Failed to fetch menus:", err);
    } finally {
      loading = false;
    }
  }

  // 日付変更時の処理
  function handleDateChange() {
    fetchMenus();
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
      month: "long",
      day: "numeric",
      weekday: "long",
    });
  }

  // 初期データ読み込み
  onMount(() => {
    fetchMenus();
  });

  let reportingId = null; // 報告処理中のメニューID
  const userId = "T00001"; // 仮のユーザーID

  // 売り切れ状態を計算
  function getSoldOutStatus(menu) {
    const soldOutCount = menu.reviewers?.length || 0;
    const availableCount = menu.unti_reviewers?.length || 0;

    if (soldOutCount === 0) {
      return null; // 売り切れ報告がなければ何も表示しない
    }

    if (soldOutCount >= 2 || soldOutCount > availableCount) {
      return "sold-out"; // 赤色状態
    }

    return "maybe-sold-out"; // 黄色状態
  }

  // 売り切れ報告を送信
  async function reportSoldOutStatus(menu, reportType) {
    if (reportingId) return;
    reportingId = menu.id;

    try {
      const response = await fetch(`${API_BASE_URL}/menu/report`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          menu_id: menu.id,
          user_id: userId,
          report_type: reportType,
        }),
      });

      if (response.ok) {
        // 成功したらメニューを再取得してUIを更新
        await fetchMenus();
      } else {
        const data = await response.json();
        error = data.error || "報告に失敗しました";
      }
    } catch (err) {
      error = `報告処理中にエラーが発生しました: ${err.message}`;
      console.error("Report error:", err);
    } finally {
      reportingId = null;
    }
  }
</script>

<div class="menu-container">
  <!-- ヘッダー -->
  <header class="menu-header">
    <h1>
      <Icon icon="ph:fork-knife" width="28" />
      今日のメニュー
    </h1>
    <p class="header-subtitle">栄養バランスを考えた美味しいメニュー</p>
  </header>

  <!-- 日付選択 -->
  <section class="date-selector">
    <div class="date-input-container">
      <label for="menu-date" class="date-label">
        <Icon icon="ph:calendar" width="20" />
        日付を選択
      </label>
      <input
        id="menu-date"
        type="date"
        bind:value={selectedDate}
        on:change={handleDateChange}
        class="date-input"
      />
    </div>
    {#if selectedDate}
      <div class="selected-date">
        <Icon icon="ph:calendar-check" width="18" />
        {formatDate(selectedDate)}
      </div>
    {/if}
  </section>

  <!-- メニュー表示 -->
  <section class="menu-content">
    {#if loading}
      <div class="loading-state">
        <Icon icon="ph:spinner" width="32" class="spinning" />
        <p>メニューを読み込み中...</p>
      </div>
    {:else if error}
      <div class="error-state">
        <Icon icon="ph:warning" width="32" />
        <h3>エラーが発生しました</h3>
        <p>{error}</p>
        <button class="retry-button" on:click={fetchMenus}>
          <Icon icon="ph:arrow-clockwise" width="16" />
          再試行
        </button>
      </div>
    {:else if menus.length === 0}
      <div class="empty-state">
        <Icon icon="ph:fork-knife" width="48" />
        <h3>メニューが見つかりません</h3>
        <p>選択した日付のメニューは登録されていません</p>
      </div>
    {:else}
      <div class="menu-grid">
        {#each menus as menu}
          {@const status = getSoldOutStatus(menu)}
          {@const soldOutCount = menu.reviewers?.length || 0}
          {@const availableCount = menu.unti_reviewers?.length || 0}
          {@const totalVotes = soldOutCount + availableCount}
          <div class="menu-card" class:sold-out={status === 'sold-out'}>
            <!-- 売り切れオーバーレイ -->
            {#if status === 'sold-out'}
              <div class="sold-out-overlay">
                <span>SOLD OUT</span>
              </div>
            {/if}

            <!-- メニュータイプバッジ -->
            <div class="menu-type {menu.type.toLowerCase()}">
              {menu.type}セット
            </div>

            <!-- メニュー情報 -->
            <div class="menu-info">
              <h2 class="menu-name">{menu.name}</h2>

              <!-- 価格とカロリー -->
              <div class="menu-details">
                <div class="price-tag">
                  <Icon icon="ph:currency-yen" width="16" />
                  ¥{menu.price}
                </div>
                <div class="calorie-tag">
                  <Icon icon="ph:flame" width="16" />
                  {menu.energy}kcal
                </div>
              </div>

              <!-- 栄養成分 -->
              <div class="nutrition-info">
                <h4>
                  <Icon icon="ph:heart" width="16" />
                  栄養成分
                </h4>
                <div class="nutrition-grid">
                  <div class="nutrition-item">
                    <span class="label">たんぱく質</span>
                    <span class="value">{menu.protein}g</span>
                  </div>
                  <div class="nutrition-item">
                    <span class="label">脂質</span>
                    <span class="value">{menu.fat}g</span>
                  </div>
                  <div class="nutrition-item">
                    <span class="label">炭水化物</span>
                    <span class="value">{menu.carb}g</span>
                  </div>
                  <div class="nutrition-item">
                    <span class="label">食塩相当量</span>
                    <span class="value">{menu.salt}g</span>
                  </div>
                </div>
              </div>

              <!-- アレルゲン情報 -->
              <div class="allergen-info">
                <h4>
                  <Icon icon="ph:warning-circle" width="16" />
                  アレルゲン情報
                </h4>
                <div class="allergen-list">
                  {formatAllergens(menu.allergens)}
                </div>
              </div>

              <!-- 売り切れ報告セクション -->
              {#if status}
                <div class="sold-out-status {status}">
                  <div class="status-header">
                    <Icon
                      icon={status === 'sold-out'
                        ? "ph:x-circle-fill"
                        : "ph:warning-circle-fill"}
                      width="20"
                    />
                    <span class="status-text">
                      {status === 'sold-out'
                        ? "売り切れ"
                        : "売り切れているかも？"}
                    </span>
                  </div>
                  <div class="status-bar">
                    <div
                      class="bar-sold-out"
                      style="width: {totalVotes > 0
                        ? (soldOutCount / totalVotes) * 100
                        : 0}%"
                    ></div>
                  </div>
                  <div class="status-votes">
                    <span>売り切れ報告: {soldOutCount}件</span>
                    <span>在庫あり報告: {availableCount}件</span>
                  </div>
                </div>
              {/if}

              <!-- 報告ボタン -->
              <div class="report-buttons">
                <button
                  class="report-button sold-out"
                  on:click={() => reportSoldOutStatus(menu, 'sold_out')}
                  disabled={reportingId === menu.id}
                >
                  <Icon icon="ph:x-circle" width="16" />
                  売り切れかも？
                </button>
                <button
                  class="report-button available"
                  on:click={() => reportSoldOutStatus(menu, 'available')}
                  disabled={reportingId === menu.id}
                >
                  <Icon icon="ph:check-circle" width="16" />
                  まだあるよ
                </button>
              </div>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </section>

  <!-- お知らせ -->
  <section class="notice-section">
    <div class="notice-card">
      <div class="notice-icon">
        <Icon icon="ph:info" width="24" />
      </div>
      <div class="notice-content">
        <h4>ご利用について</h4>
        <ul>
          <li>メニューは変更になる場合があります</li>
          <li>売り切れの際はご了承ください</li>
          <li>アレルギーをお持ちの方は事前にご確認ください</li>
        </ul>
      </div>
    </div>
  </section>
</div>

<style>
  .menu-container {
    min-height: 100vh;
    padding: 1rem;
    max-width: 800px;
    margin: 0 auto;
  }

  /* ヘッダー */
  .menu-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .menu-header h1 {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    font-size: 1.6rem;
    font-weight: bold;
    margin: 0 0 0.5rem 0;
    color: #333;
  }

  .header-subtitle {
    margin: 0;
    color: #666;
    font-size: 0.9rem;
  }

  /* 日付選択 */
  .date-selector {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .date-input-container {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .date-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
    color: #333;
    font-size: 0.9rem;
  }

  .date-input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
    background: #f8f9fa;
  }

  .selected-date {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #007bff;
    font-weight: 500;
    background: #e3f2fd;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
  }

  /* ステータス表示 */
  .loading-state,
  .error-state,
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 3rem 1rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .loading-state {
    color: #666;
  }

  .error-state {
    color: #dc3545;
  }

  .empty-state {
    color: #666;
  }

  .error-state h3,
  .empty-state h3 {
    margin: 1rem 0 0.5rem 0;
    font-size: 1.2rem;
  }

  .error-state p,
  .empty-state p {
    margin: 0 0 1rem 0;
  }

  .retry-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: #dc3545;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
  }

  .retry-button:hover {
    background: #c82333;
  }

  /* メニューグリッド */
  .menu-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .menu-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
  }

  .menu-card:hover {
    transform: translateY(-2px);
  }

  /* メニュータイプ */
  .menu-type {
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    text-align: center;
    color: white;
  }

  .menu-type.a {
    background: linear-gradient(135deg, #007bff, #0056b3);
  }

  .menu-type.b {
    background: linear-gradient(135deg, #28a745, #1e7e34);
  }

  /* メニュー情報 */
  .menu-info {
    padding: 1.5rem;
  }

  .menu-name {
    font-size: 1.3rem;
    font-weight: 600;
    margin: 0 0 1rem 0;
    color: #333;
  }

  .menu-details {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .price-tag,
  .calorie-tag {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 500;
    font-size: 0.9rem;
  }

  .price-tag {
    background: #fff3cd;
    color: #856404;
  }

  .calorie-tag {
    background: #d1ecf1;
    color: #0c5460;
  }

  /* 栄養情報 */
  .nutrition-info,
  .allergen-info {
    margin-bottom: 1.5rem;
  }

  .nutrition-info h4,
  .allergen-info h4 {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1rem;
    font-weight: 600;
    margin: 0 0 0.75rem 0;
    color: #333;
  }

  .nutrition-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }

  .nutrition-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem;
    background: #f8f9fa;
    border-radius: 6px;
  }

  .nutrition-item .label {
    font-size: 0.85rem;
    color: #666;
  }

  .nutrition-item .value {
    font-weight: 600;
    color: #333;
  }

  .allergen-list {
    background: #fff5f5;
    border: 1px solid #fecaca;
    border-radius: 6px;
    padding: 0.75rem;
    color: #dc3545;
    font-weight: 500;
  }

  /* 売り切れ報告セクション */
  .sold-out-status {
    margin-top: 1.5rem;
    padding: 1rem;
    border-radius: 8px;
  }

  .sold-out-status.sold-out {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
  }

  .sold-out-status.maybe-sold-out {
    background: #fff3cd;
    border: 1px solid #ffeeba;
    color: #856404;
  }

  .status-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: bold;
    margin-bottom: 0.75rem;
  }

  .status-bar {
    width: 100%;
    height: 8px;
    background: #e9ecef;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 0.5rem;
  }

  .bar-sold-out {
    height: 100%;
    background: #dc3545;
  }

  .status-votes {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
  }

  .report-buttons {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .report-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.75rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
    transition: background-color 0.2s;
  }

  .report-button.sold-out {
    background: #ffebee;
    color: #c62828;
  }

  .report-button.sold-out:hover:not(:disabled) {
    background: #ffcdd2;
  }

  .report-button.available {
    background: #e8f5e9;
    color: #2e7d32;
  }

  .report-button.available:hover:not(:disabled) {
    background: #c8e6c9;
  }

  .report-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* お知らせセクション */
  .notice-section {
    margin-top: 2rem;
  }

  .notice-card {
    display: flex;
    gap: 1rem;
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .notice-icon {
    flex-shrink: 0;
    width: 40px;
    height: 40px;
    background: #e3f2fd;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #007bff;
  }

  .notice-content h4 {
    margin: 0 0 0.75rem 0;
    font-size: 1rem;
    font-weight: 600;
    color: #333;
  }

  .notice-content ul {
    margin: 0;
    padding-left: 1.25rem;
    color: #666;
  }

  .notice-content li {
    margin-bottom: 0.25rem;
    font-size: 0.9rem;
    line-height: 1.4;
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
  @media (min-width: 768px) {
    .menu-container {
      padding: 2rem;
    }

    .menu-grid {
      grid-template-columns: repeat(2, 1fr);
    }

    .nutrition-grid {
      grid-template-columns: repeat(4, 1fr);
    }

    .date-input-container {
      justify-content: center;
    }

    .date-input {
      max-width: 200px;
    }
  }

  @media (min-width: 1024px) {
    .menu-container {
      max-width: 1000px;
    }

    .nutrition-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
</style>
