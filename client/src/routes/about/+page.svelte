<script lang="ts">
  type Menu = {
    id: string;
    type: string;
    name: string;
    price: number;
    energy: number;
    protein: number;
    fat: number;
    carb: number;
    salt: number;
    allergens: string[];
  };

  const res = async () => {
    const res = await fetch("http://localhost:8000/menu/permanent/all");
    if (res.ok) {
      const menus: Menu[] = await res.json();
      return menus;
    } else {
      console.error("Failed to fetch menu data");
      return null;
    }
  };
</script>

<h1>通常メニュー</h1>
<p>こちらでは、通常メニューの情報を表示します。</p>

{#await res()}
  <p>Loading...</p>
{:then menus}
  {#if menus.length > 0 && menus !== null}
    <div class="menu-container">
      {#each menus as menu}
        <div class="menu-card">
          <div class="menu-title">
            <p>{menu.type}</p>
            <div class="menu-details">
              <h2>{menu.name}</h2>
              <p>{menu.price}円</p>
            </div>
          </div>
          <p>アレルゲン:</p>
          <ul>
            {#each menu.allergens as allergen}
              <li>
                {allergen}
              </li>
            {/each}
          </ul>
          <div class="menu-nutrition">
            <!-- 成分表示 -->
            <p>エネルギー: {menu.energy}kcal</p>
            <p>タンパク質: {menu.protein}g</p>
            <p>脂質: {menu.fat}g</p>
            <p>炭水化物: {menu.carb}g</p>
            <p>食塩相当量: {menu.salt}g</p>
          </div>
        </div>
      {/each}
    </div>
  {:else}
    <p>メニューはありません。</p>
  {/if}
{:catch error}
  <p>Error: {error.message}</p>
{/await}

<style>
  .menu-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    padding: 20px;
  }
</style>
