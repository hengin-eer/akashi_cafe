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
      energy: 700,
      protein: 12,
      fat: 20,
      carb: 130,
      salt: 4.0,
    },
    {
      name: "ポークカツカレー",
      price: 380,
      allergen: true,
      soldOut: false,
      energy: 770,
      protein: 14.5,
      fat: 22.3,
      carb: 131,
      salt: 4.8,
    },
    {
      name: "親子丼",
      price: 350,
      allergen: true,
      soldOut: false,
      energy: 550,
      protein: 18,
      fat: 12,
      carb: 80,
      salt: 2.5,
    },
    {
      name: "かつ丼",
      price: 350,
      allergen: true,
      soldOut: false,
      energy: 700,
      protein: 22,
      fat: 24,
      carb: 85,
      salt: 3.0,
    },
    {
      name: "醤油らーめん",
      price: 250,
      allergen: true,
      soldOut: false,
      energy: 480,
      protein: 14,
      fat: 16,
      carb: 65,
      salt: 5.5,
    },
    {
      name: "かけうどん・そば",
      price: 200,
      allergen: true,
      soldOut: false,
      energy: 300,
      protein: 8,
      fat: 2,
      carb: 60,
      salt: 2.0,
    },
  ];

  let selectedMenu = null;

  function openModal(menu) {
    selectedMenu = menu;
  }

  function closeModal() {
    selectedMenu = null;
  }
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
            <!-- なんか高さ合わないから空のバッジ入れて調整してる -->
            <span class="badge" style="visibility: hidden;"> placeholder </span>
          {/if}
        </div>
        <div>{menu.name}</div>
        <div class="price">￥{menu.price}</div>
      </button>
    {/each}
  </div>
</div>

{#if selectedMenu}
  <div class="modal-overlay" on:click={closeModal}>
    <div class="modal" on:click|stopPropagation>
      <h2>{selectedMenu.name}</h2>
      <p style="font-size: 1.2rem; font-weight: bold;">
        ￥{selectedMenu.price}
      </p>
      <p><strong>特定アレルゲン:</strong> 小麦、卵、乳</p>
      <p><strong>エネルギー:</strong> {selectedMenu.energy}[kcal]</p>
      <p><strong>タンパク質:</strong> {selectedMenu.protein}[g]</p>
      <p><strong>脂質:</strong> {selectedMenu.fat}[g]</p>
      <p><strong>炭水化物:</strong> {selectedMenu.carb}[g]</p>
      <p><strong>食塩相当量:</strong> {selectedMenu.salt}[g]</p>

      <div class="sold-out-info">
        <p><strong>売り切れ情報</strong></p>
        <p>投稿数：3件</p>
        <p>信頼性：高い</p>
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
    padding: 1.5rem;
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
</style>
