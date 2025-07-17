<script>
  // 特にロジックは不要だが、ここにGoogleログインの処理などを書けます
  const handleGoogleLogin = () => {
    alert("Googleログイン処理をここに実装してください。");
  };
</script>

<div class="container">
  <h1>明石高専 学生食堂システム</h1>

  <h2>ユーザログインページ</h2>

  <div class="box">
    <p>🖐 <b>ログインするメリット</b></p>
    <p>ログインすることで、<b>認証ユーザ</b>となることが出来ます。</p>
    <p>
      売り切れ投稿の信ぴょう性が高まり、多くの利用者へ貢献することが出来ます。
    </p>
  </div>

  <div class="button" on:click={handleGoogleLogin}>
    <img
      src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
      alt="Googleアイコン"
    />
    Googleで続ける
  </div>

  <a class="admin-link" href="/admin">管理者ページはこちら</a>
</div>

<style>
  :global(body) {
    margin: 0;
    font-family: "Hiragino Kaku Gothic ProN", Meiryo, sans-serif;
    background-color: #f7f6fb;
  }

  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    min-height: 100vh;
    padding: 40px 20px;
    box-sizing: border-box;
  }

  h1 {
    font-size: 1.5em;
    margin-bottom: 60px;
    text-align: center;
    color: #000;
  }

  h2 {
    font-size: 1.2em;
    margin-bottom: 20px;
    color: #000;
  }

  .box {
    background-color: #f1effa;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 30px;
    max-width: 400px;
    text-align: left;
  }

  .box p {
    margin: 0.5em 0;
    font-size: 0.9em;
    color: #333;
  }

  .button {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 12px 20px;
    cursor: pointer;
    font-size: 1em;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
    margin-bottom: 20px;
    transition: background-color 0.2s;
  }

  .button:hover {
    background-color: #f0f0f0;
  }

  .button img {
    width: 20px;
    margin-right: 10px;
  }

  .admin-link {
    font-size: 0.95em;
    color: #000;
    text-decoration: underline;
  }

  .admin-link:hover {
    color: #333;
  }
</style>
