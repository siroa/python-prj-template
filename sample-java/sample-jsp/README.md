# JSP / Servlet サンプルアプリケーション (JDK 8)

Java (Servlet 3.1) をコントローラ、JSP (JSTL 1.2) をビュー、JavaBeans をモデルとした MVC モデル 2 構成のメモ管理 Web アプリケーションです。
本プロジェクトは **Java 8 (JDK 8)** および **Java EE (javax.* 名前空間)** を前提に構成されています。

---

## 1. 動作環境要件

- **Java (JDK):** 1.8 (Java 8)
- **ビルドツール:** Apache Maven 3.6 以上
- **Servlet コンテナ:** Apache Tomcat 8.5 または 9.0
  - ※ Tomcat 10 以降は Jakarta EE (`jakarta.*`) 規格となるため動作しません。

---

## 2. 依存パッケージおよびプラグイン一覧

### アプリケーション / テスト依存ライブラリ

| グループID / アーティファクトID | バージョン | スコープ | 用途 / 備考 |
| :--- | :--- | :--- | :--- |
| `javax.servlet:javax.servlet-api` | `3.1.0` | `provided` | Java EE 7 Servlet 仕様（Tomcat から提供） |
| `javax.servlet:jstl` | `1.2` | `compile` | JSP 標準タグライブラリ (JSTL) |
| `org.junit.jupiter:junit-jupiter` | `5.10.2` | `test` | 単体テストフレームワーク (JUnit 5) |
| `org.mockito:mockito-junit-jupiter` | `4.11.0` | `test` | サーブレットモック作成 (※4系はJDK 8最終対応ライン) |

### ビルドプラグイン

| プラグイン名 | バージョン | 役割 |
| :--- | :--- | :--- |
| `maven-compiler-plugin` | `3.13.0` | ソース・ターゲット `1.8` でのコンパイル |
| `maven-war-plugin` | `3.3.2` | Web アプリケーションアーカイブ (`.war`) の生成 |
| `maven-surefire-plugin` | `3.1.2` | `mvn test` による JUnit 5 テストの実行 |

---

## 3. プロジェクト構成

```text
jsp-servlet-jdk8-sample/
├── pom.xml
├── README.md
└── src/
    ├── main/
    │   ├── java/
    │   │   └── com/
    │   │       └── example/
    │   │           ├── model/
    │   │           │   └── Item.java          # データモデル (JavaBeans)
    │   │           └── servlet/
    │   │               └── ItemServlet.java   # コントローラ (HttpServlet)
    │   └── webapp/
    │       └── WEB-INF/
    │           └── views/
    │               └── items.jsp              # ビュー (JSP + JSTL)
    └── test/
        └── java/
            └── com/
                └── example/
                    ├── model/
                    │   └── ItemTest.java          # モデルの単体テスト
                    └── servlet/
                        └── ItemServletTest.java   # サーブレットの単体テスト (Mockito)
```

---

## 4. Maven コマンド実行例

ターミナル（プロジェクトルートディレクトリ）で実行します。

### ソースコードのコンパイル
```bash
mvn compile
```

### 全テストの実行
```bash
mvn test
```

### 特定のテストクラスのみ実行
```bash
# ItemServletTest のみ実行する場合
mvn test -Dtest=ItemServletTest

# ItemTest のみ実行する場合
mvn test -Dtest=ItemTest
```

### WAR ファイルのビルド（パッケージング）
テストを実行してから `target/` 配下に WAR ファイルを生成します。
```bash
mvn clean package
```

### テストをスキップしてビルド
```bash
mvn clean package -DskipTests
```

### 生成物のクリーン（ビルド成果物の破棄）
```bash
mvn clean
```

---

## 5. デプロイと動作確認

1. **WAR ファイルの配置**
   `mvn clean package` 実行後、生成された `target/jsp-servlet-jdk8-sample.war` を Tomcat の `webapps` ディレクトリにコピーします。

   ```bash
   cp target/jsp-servlet-jdk8-sample.war /path/to/tomcat/webapps/
   ```

2. **Tomcat の起動**
   ```bash
   # Linux / macOS
   /path/to/tomcat/bin/startup.sh

   # Windows
   /path/to/tomcat/bin/startup.bat
   ```

3. **ブラウザでのアクセス**
   ```text
   http://localhost:8080/jsp-servlet-jdk8-sample/items
   ```

---

## 6. よくあるトラブルシューティング

### Q1. `cannot find symbol: class ItemServlet` 等のエラーでテストが失敗する
- **原因:** ディレクトリ構造が `src/test/java/com/...` ではなく、二重階層（例: `src/test/java/test/java/...`）になっている可能性があります。
- **対処法:** `src/test/java` 直下にパッケージルート（`com/`）が配置されているか確認してください。

### Q2. Tomcat 10 にデプロイしたら `ClassNotFoundException: javax.servlet.Servlet` が発生する
- **原因:** Tomcat 10 以降は Jakarta EE (`jakarta.*`) を要求するため、本アプリの `javax.*` はロードできません。
- **対処法:** Apache Tomcat 8.5 または 9.0 をご利用ください。