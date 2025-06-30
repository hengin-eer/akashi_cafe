<script>
  import Icon from "@iconify/svelte";

  export let data;
  const selectedDate = data.date;

  const today = new Date();
  const thisMonth = today.getMonth() + 1;

  // TODO: selectedDateを使って本番データを取得する

  let menus = [
    {
      name: "カレーライス(中辛)",
      price: 300,
      allergen: true,
      soldOut: true,
    },
    {
      name: "ポークカツカレー",
      price: 380,
      allergen: true,
      soldOut: false,
    },
    {
      name: "親子丼",
      price: 350,
      allergen: true,
      soldOut: false,
    },
    {
      name: "かつ丼",
      price: 350,
      allergen: true,
      soldOut: false,
    },
    {
      name: "醤油らーめん",
      price: 250,
      allergen: true,
      soldOut: false,
    },
    {
      name: "かけうどん・そば",
      price: 200,
      allergen: true,
      soldOut: false,
    },
  ];
</script>

<div class="container">
  <h1>明石高専 学生食堂システム</h1>
  <p style="font-weight: bold; font-size: 1.25rem;">
    {thisMonth}月{selectedDate ? selectedDate : "?"}日のメニュー
  </p>

  <p style="font-size: 0.85rem; color: #666;">
    各メニューの詳細情報や、売り切れ情報の送信はタップすることで確認できます。
  </p>

  <div class="menu-grid">
    {#each menus as menu}
      <button class="menu-card {menu.soldOut && 'sold-out'}">
        <div style="display: flex; gap: 0.3rem; flex-wrap: wrap;">
          {#if menu.soldOut}
            <span class="badge red">
              <Icon icon="ph:x-circle" width="16" />
              売り切れ
            </span>
          {/if}
          {#if menu.allergen}
            <span class="badge">アレルゲン有</span>
          {/if}
        </div>
        <div>{menu.name}</div>
        <div class="price">￥{menu.price}</div>
      </button>
    {/each}
  </div>
</div>

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
</style>
