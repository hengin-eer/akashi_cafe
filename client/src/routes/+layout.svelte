<script>
  import Icon from "@iconify/svelte";
  import { page } from "$app/stores";

  // 現在のページパスを取得
  $: currentPath = $page.url.pathname;

  // 管理者ページかどうかを判定
  $: isAdminPage = currentPath.startsWith("/admin");
</script>

{#if !isAdminPage}
  <div class="app-layout">
    <!-- メインコンテンツ -->
    <main class="main-content">
      <slot />
    </main>

    <!-- ボトムナビゲーション -->
    <nav class="bottom-nav">
      <a href="/" class="nav-item" class:active={currentPath === "/"}>
        <Icon icon="ph:house-fill" width="24" />
        <span>ホーム</span>
      </a>

      <a href="/menu" class="nav-item" class:active={currentPath === "/menu"}>
        <Icon icon="ph:fork-knife-fill" width="24" />
        <span>メニュー</span>
      </a>

      <a href="/login" class="nav-item" class:active={currentPath === "/login"}>
        <Icon icon="ph:user-circle-fill" width="24" />
        <span>ログイン</span>
      </a>
    </nav>
  </div>
{:else}
  <!-- 管理者ページの場合は何もしない（管理者レイアウトが適用される） -->
  <slot />
{/if}

<style>
  :global(body) {
    margin: 0;
    font-family: "Hiragino Kaku Gothic ProN", Meiryo, sans-serif;
    background-color: #f7f6fb;
  }

  .app-layout {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    padding-bottom: 80px; /* ボトムナビの高さ分 */
  }

  .main-content {
    flex: 1;
    width: 100%;
    max-width: 100%;
    overflow-x: hidden;
  }

  /* ボトムナビゲーション */
  .bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 80px;
    background: white;
    border-top: 1px solid #e9ecef;
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 0 1rem;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
    z-index: 1000;
  }

  .nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    color: #666;
    transition: all 0.2s ease;
    padding: 0.5rem;
    border-radius: 8px;
    min-width: 60px;
    gap: 0.25rem;
  }

  .nav-item span {
    font-size: 0.75rem;
    font-weight: 500;
  }

  .nav-item:hover {
    color: #007bff;
    background: #f8f9ff;
  }

  .nav-item.active {
    color: #007bff;
    background: #e3f2fd;
  }

  .nav-item.active span {
    font-weight: 600;
  }

  /* レスポンシブ対応（デスクトップでは通常のナビゲーション） */
  @media (min-width: 768px) {
    .app-layout {
      padding-bottom: 0;
    }

    .bottom-nav {
      position: static;
      height: auto;
      background: white;
      border-top: 1px solid #e9ecef;
      border-bottom: 1px solid #e9ecef;
      flex-direction: row;
      justify-content: center;
      gap: 2rem;
      padding: 1rem;
      margin-top: auto;
    }

    .nav-item {
      flex-direction: row;
      gap: 0.5rem;
      padding: 0.75rem 1.5rem;
    }

    .nav-item span {
      font-size: 1rem;
    }
  }
</style>
