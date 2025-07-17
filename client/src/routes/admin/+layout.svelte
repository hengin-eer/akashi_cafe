<script>
  import Icon from "@iconify/svelte";
  import { page } from "$app/stores";

  // 現在のページパスを取得
  $: currentPath = $page.url.pathname;
</script>

<div class="admin-layout">
  <!-- ヘッダー -->
  <header class="admin-header">
    <div class="header-container">
      <div class="logo">
        <Icon icon="ph:coffee" width="24" />
        <span>明石カフェ管理システム</span>
      </div>

      <nav class="admin-nav">
        <a
          href="/admin"
          class="nav-link"
          class:active={currentPath === "/admin"}
        >
          <Icon icon="ph:house" width="20" />
          ダッシュボード
        </a>
        <a
          href="/admin/menu/upload"
          class="nav-link"
          class:active={currentPath === "/admin/menu/upload"}
        >
          <Icon icon="ph:upload" width="20" />
          メニュー追加
        </a>
        <a
          href="/admin/menu/list"
          class="nav-link"
          class:active={currentPath === "/admin/menu/list"}
        >
          <Icon icon="ph:list-checks" width="20" />
          メニュー管理
        </a>
      </nav>

      <div class="header-actions">
        <a href="/login" class="logout-link">
          <Icon icon="ph:sign-out" width="20" />
          ログアウト
        </a>
      </div>
    </div>
  </header>

  <!-- メインコンテンツ -->
  <main class="admin-main">
    <div class="content-container">
      <slot />
    </div>
  </main>

  <!-- フッター -->
  <footer class="admin-footer">
    <div class="footer-container">
      <p>&copy; 2025 明石高専 学生食堂システム. All rights reserved.</p>
    </div>
  </footer>
</div>

<style>
  :global(body) {
    margin: 0;
    font-family: sans-serif;
    background-color: #f7f6fb;
  }

  .admin-layout {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  /* ヘッダー */
  .admin-header {
    background: white;
    border-bottom: 1px solid #e9ecef;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .header-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    color: #333;
  }

  .admin-nav {
    display: flex;
    gap: 1rem;
  }

  .nav-link {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    text-decoration: none;
    color: #666;
    border-radius: 8px;
    transition: all 0.2s;
    font-weight: 500;
  }

  .nav-link:hover {
    color: #007bff;
    background: #f8f9ff;
  }

  .nav-link.active {
    color: #007bff;
    background: #e3f2fd;
  }

  .header-actions {
    display: flex;
    align-items: center;
  }

  .logout-link {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    text-decoration: none;
    color: #666;
    border-radius: 8px;
    transition: all 0.2s;
    font-weight: 500;
  }

  .logout-link:hover {
    color: #dc3545;
    background: #fff5f5;
  }

  /* メインコンテンツ */
  .admin-main {
    flex: 1;
    padding: 2rem 0;
  }

  .content-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
  }

  /* フッター */
  .admin-footer {
    background: white;
    border-top: 1px solid #e9ecef;
    margin-top: auto;
  }

  .footer-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem 2rem;
    text-align: center;
    color: #666;
    font-size: 0.9rem;
  }

  /* レスポンシブ */
  @media (max-width: 768px) {
    .header-container {
      padding: 1rem;
      flex-direction: column;
      gap: 1rem;
    }

    .admin-nav {
      order: 2;
      flex-wrap: wrap;
      justify-content: center;
    }

    .header-actions {
      order: 3;
    }

    .content-container {
      padding: 0 1rem;
    }

    .footer-container {
      padding: 1rem;
    }

    .nav-link {
      font-size: 0.9rem;
      padding: 0.4rem 0.8rem;
    }
  }

  @media (max-width: 480px) {
    .logo {
      font-size: 1rem;
    }

    .nav-link {
      flex-direction: column;
      gap: 0.25rem;
      font-size: 0.8rem;
      padding: 0.5rem;
      text-align: center;
    }

    .logout-link {
      flex-direction: column;
      gap: 0.25rem;
      font-size: 0.8rem;
      padding: 0.5rem;
      text-align: center;
    }
  }
</style>
