<script>
  const currentMonth = new Date().getMonth() + 1;
</script>

<!-- TODO: コンポーネントとして共通化せねば -->
<header class="header">明石高専 学生食堂システム</header>

<main class="main">
  <section class="card">
    <h2>{currentMonth}月のメニュー</h2>
    <p>日付や値段で1か月のメニューが絞り込める！</p>
    <button>
      <a href="/menu"> メニューの日付を選択する </a>
    </button>
  </section>

  <section class="card">
    <h2>ユーザログイン</h2>
    <p>メニュー情報の編集や売り切れ情報の管理など</p>
    <button>
      <a href="/login">ログインページへ</a>
    </button>
  </section>
</main>

<style>
  .header {
    background-color: #f1f0f6;
    padding: 20px;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    border-bottom: 1px solid #ddd;
  }

  .main {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px 16px;
  }

  .card {
    background-color: #f1f0f6;
    border-radius: 16px;
    padding: 24px 16px;
    margin-bottom: 24px;
    max-width: 420px;
    width: 100%;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    text-align: center;
  }

  .card h2 {
    font-size: 20px;
    margin-bottom: 8px;
  }

  .card p {
    font-size: 14px;
    margin-bottom: 16px;
  }

  .card button {
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 12px;
    padding: 10px 20px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }

  .card button:hover {
    background-color: #f0f0f0;
  }

  .card button a {
    text-decoration: none;
    color: black;
    display: inline-block;
  }
</style>
