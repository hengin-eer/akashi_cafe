<script>
  import Icon from "@iconify/svelte";
  import { onMount } from "svelte";

  const today = new Date();
  const year = today.getFullYear();
  const month = today.getMonth();

  const monthStr = String(month + 1).padStart(2, "0");
  const minDate = `${year}-${monthStr}-01`;
  const lastDay = new Date(year, month + 1, 0).getDate();
  const maxDate = `${year}-${monthStr}-${String(lastDay).padStart(2, "0")}`;

  let selectedDate = today.toISOString().split("T")[0];

  function onDateChange(e) {
    selectedDate = e.target.value;
    fetchMenus();
  }

  const thisMonth = Number(monthStr);

  // APIベースURL
  const API_BASE_URL = "http://localhost:8000";

  let menus = [];
  let loading = false;
  let error = null;
  let restaurantStatus = "open"; // "open", "closed", "error"

  // 日付から曜日を取得
  function getDayOfWeek(dateString) {
    const date = new Date(dateString);
    const days = ["日", "月", "火", "水", "木", "金", "土"];
    return days[date.getDay()];
  }

  // 土日判定
  function isWeekend(dateString) {
    const date = new Date(dateString);
    const dayOfWeek = date.getDay();
    return dayOfWeek === 0 || dayOfWeek === 6; // 0=日曜日, 6=土曜日
  }

  // 祝日判定（簡易版 - 実際にはより詳細な祝日データが必要）
  function isHoliday(dateString) {
    // 今回は簡易的に祝日判定を行います
    // 実際のプロダクションでは祝日APIや祝日ライブラリを使用することを推奨
    const date = new Date(dateString);
    const month = date.getMonth() + 1;
    const day = date.getDate();

    // 一部の固定祝日の例
    const holidays = [
      { month: 1, day: 1 }, // 元日
      { month: 5, day: 3 }, // 憲法記念日
      { month: 5, day: 4 }, // みどりの日
      { month: 5, day: 5 }, // こどもの日
      { month: 12, day: 23 }, // 天皇誕生日
    ];

    return holidays.some(
      (holiday) => holiday.month === month && holiday.day === day,
    );
  }

  // バックエンドAPIからメニューデータを取得
  async function fetchMenus() {
    loading = true;
    error = null;
    restaurantStatus = "open";

    try {
      const response = await fetch(`${API_BASE_URL}/menu/${selectedDate}`);
      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();

      // エラーレスポンスをチェック
      if (data.error) {
        throw new Error(data.error);
      }

      // 新しいAPIレスポンス形式をチェック
      if (data.status) {
        // 新しい形式: {status: "open/closed", message: "...", menus: [...]}
        if (data.status === "closed") {
          restaurantStatus = "closed";
          menus = [];
          return;
        }

        restaurantStatus = "open";
        const menusData = data.menus || [];

        // APIレスポンスを画面表示用の形式に変換
        menus = menusData.map((item) => ({
          id: item.id,
          name: item.name,
          price: item.price,
          allergens: item.allergens || [],
          soldOut: false, // 現在のAPIには売り切れ情報がないため、デフォルトでfalse
          energy: item.energy,
          protein: item.protein,
          fat: item.fat,
          carb: item.carb,
          salt: item.salt,
          type: item.type,
        }));
      } else {
        // 古い形式: 直接配列が返される場合
        if (Array.isArray(data)) {
          restaurantStatus = "open";
          menus = data.map((item) => ({
            id: item.id,
            name: item.name,
            price: item.price,
            allergens: item.allergens || [],
            soldOut: false,
            energy: item.energy,
            protein: item.protein,
            fat: item.fat,
            carb: item.carb,
            salt: item.salt,
            type: item.type,
          }));
        } else {
          throw new Error("予期しないレスポンス形式です");
        }
      }
    } catch (err) {
      error = err.message;
      restaurantStatus = "error";
      console.error("Failed to fetch menus:", err);
      // エラー時は空配列を設定
      menus = [];
    } finally {
      loading = false;
    }
  }

  // コンポーネントマウント時に初期データを取得
  onMount(() => {
    fetchMenus();
  });

  let selectedMenu = null;

  function openModal(menu) {
    selectedMenu = menu;
  }

  function closeModal() {
    selectedMenu = null;
  }

  // TODO: 実際の売り切れ投稿数を取得して動的に変更する必要がある
  let postCount = 3;

  // 投稿数に基づいて信頼性を判定（1件または10件以上は信頼性が低い）
  function getReliability(count) {
    if (count === 1 || count >= 10) {
      return "低い";
    } else if (count >= 2 && count <= 9) {
      return "高い";
    }
    return "低い";
  }

  $: reliability = getReliability(postCount);
</script>

<div class="container">
  <h1>明石高専 学生食堂システム</h1>
  <label for="menu-date">日付を選択：</label>
  <input
    id="menu-date"
    type="date"
    bind:value={selectedDate}
    min={minDate}
    max={maxDate}
    on:change={onDateChange}
  />
  <p style="font-weight: bold; font-size: 1.25rem;">
    {thisMonth}月{selectedDate.split("-")[2]}日のメニュー
  </p>

  <p style="font-size: 0.85rem; color: #666;">
    各メニューの詳細情報や、売り切れ情報の送信はタップすることで確認できます。
  </p>

  {#if loading}
    <div class="loading">
      <p>メニューを読み込み中...</p>
    </div>
  {:else if restaurantStatus === "error"}
    <div class="error">
      <p>エラーが発生しました: {error}</p>
      <button on:click={fetchMenus} class="retry-button">再試行</button>
    </div>
  {:else if restaurantStatus === "closed"}
    <div class="closed-day">
      {#if isWeekend(selectedDate)}
        <p>{getDayOfWeek(selectedDate)}曜日は</p>
        <p>お休みしています</p>
      {:else if isHoliday(selectedDate)}
        <p>祝日なので</p>
        <p>お休みしています</p>
      {:else}
        <p>本日は</p>
        <p>お休みしています</p>
      {/if}
    </div>
  {:else if menus.length === 0}
    <div class="no-menu">
      <p>この日のメニューはありません。</p>
    </div>
  {:else}
    <div class="menu-grid">
      {#each menus as menu}
        <button
          class="menu-card {menu.soldOut && 'sold-out'}"
          on:click={() => openModal(menu)}
        >
          <div style="display: flex; gap: 0.3rem; flex-wrap: wrap;">
            {#if menu.soldOut}
              <span class="badge red">
                <Icon icon="ph:x-circle" width="16" />
                売り切れ
              </span>
            {:else}
              <!-- レイアウトの高さを統一するための非表示バッジ -->
              <span class="badge" style="visibility: hidden;">
                placeholder
              </span>
            {/if}
          </div>
          <div>{menu.name}</div>
          <div class="price">￥{menu.price}</div>
        </button>
      {/each}
    </div>
  {/if}
</div>

{#if selectedMenu}
  <div class="modal-overlay" on:click={closeModal}>
    <div class="modal" on:click|stopPropagation>
      <h2>{selectedMenu.name}</h2>
      <p style="font-size: 1.2rem; font-weight: bold;">
        ￥{selectedMenu.price}
      </p>
      <p>
        <strong>特定アレルゲン:</strong>
        {#if selectedMenu.allergens && selectedMenu.allergens.length > 0}
          {selectedMenu.allergens.join("、")}
        {:else}
          なし
        {/if}
      </p>
      <p><strong>エネルギー:</strong> {selectedMenu.energy}[kcal]</p>
      <p><strong>タンパク質:</strong> {selectedMenu.protein}[g]</p>
      <p><strong>脂質:</strong> {selectedMenu.fat}[g]</p>
      <p><strong>炭水化物:</strong> {selectedMenu.carb}[g]</p>
      <p><strong>食塩相当量:</strong> {selectedMenu.salt}[g]</p>

      <div class="sold-out-info">
        <p><strong>売り切れ情報</strong></p>
        <p>投稿数：3件</p>
        <p
          style="color: {reliability === '高い'
            ? 'red'
            : 'black'}; font-weight: bold;"
        >
          信頼性：{reliability}
        </p>

        <button class="send-button">売り切れデータを送信</button>
      </div>

      <button class="close-button" on:click={closeModal}>閉じる</button>
    </div>
  </div>
{/if}

<style>
  .container {
    max-width: 480px;
    margin: auto;
    padding: 1rem;
    font-family: sans-serif;
  }

  h1 {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }

  .menu-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }

  .menu-card {
    border-radius: 12px;
    padding: 1rem;
    background: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    position: relative;
    text-align: left;
    cursor: pointer;
    border: none;
  }

  .menu-card.sold-out {
    background: #c3bebe;
  }

  .badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.75rem;
    padding: 0.2rem 0.5rem;
    border-radius: 999px;
    background: #ddd;
    margin-bottom: 0.5rem;
  }

  .badge.red {
    background: #e74c3c;
    color: white;
  }

  .price {
    font-size: 1.1rem;
    font-weight: bold;
    margin-top: 0.5rem;
  }

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
    z-index: 100;
  }

  .modal {
    background: #fff;
    border-radius: 16px;
    padding: 3rem;
    max-width: 90%;
    width: 400px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
  }

  .sold-out-info {
    margin-top: 1rem;
    padding: 0.75rem;
    background: #f0f0f0;
    border-radius: 8px;
    font-size: 0.9rem;
  }

  .send-button {
    margin-top: 0.5rem;
    background: #007bff;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    border: none;
    cursor: pointer;
  }

  .close-button {
    margin-top: 1rem;
    padding: 0.4rem 1rem;
    border: none;
    background: #aaa;
    color: white;
    border-radius: 8px;
    cursor: pointer;
  }

  .loading,
  .error,
  .no-menu,
  .closed-day {
    text-align: center;
    padding: 2rem;
    margin: 1rem 0;
    border-radius: 8px;
  }

  .loading {
    background: #f8f9fa;
    color: #666;
  }

  .error {
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }

  .no-menu {
    background: #d1ecf1;
    color: #0c5460;
    border: 1px solid #bee5eb;
  }

  .closed-day {
    background: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
  }

  .closed-day p {
    margin: 0.5rem 0;
    font-size: 1.2rem;
    font-weight: bold;
  }

  .closed-day p:first-child {
    font-size: 1.4rem;
  }

  .retry-button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background: #dc3545;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .retry-button:hover {
    background: #c82333;
  }
</style>
