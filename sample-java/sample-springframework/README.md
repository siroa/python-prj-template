# Spring MVC + JSP サンプルアプリケーション (JDK 8)

純粋な Spring Framework 5 (Spring MVC) をコントローラ、JSP (JSTL 1.2) をビュー、JavaBeans をモデルとした Web アプリケーションのサンプル構成です。  
Spring Boot を使用せず、Servlet 3.0+ の Java Config（`web.xml` 不要構成）を採用し、**Java 8 (JDK 8)** および **Java EE 7/8（`javax.*` 名前空間）** を前提としています。

---

## 1. 動作環境要件

* **Java (JDK):** 1.8 (Java 8)
* **ビルドツール:** Apache Maven 3.6 以上
* **サーブレットコンテナ:** Apache Tomcat 8.5 または Tomcat 9.0
  * ※Tomcat 10 以降は Jakarta EE (`jakarta.*`) 仕様となるため、本 WAR をそのまま稼働させることはできません。

---

## 2. 依存パッケージおよびプラグイン一覧

### アプリケーション依存ライブラリ

| グループID / アーティファクトID | バージョン | スコープ | 用途 / 備考 |
| :--- | :--- | :--- | :--- |
| `org.springframework:spring-webmvc` | `5.3.39` | `compile` | Spring MVC コア、DispatcherServlet、ViewResolver |
| `javax.servlet:javax.servlet-api` | `3.1.0` | `provided` | サーブレット API（実行コンテナ側から提供） |
| `javax.servlet:jstl` | `1.2` | `compile` | JSP 標準タグライブラリ (JSTL) |

### テスト依存ライブラリ

| グループID / アーティファクトID | バージョン | スコープ | 用途 / 備考 |
| :--- | :--- | :--- | :--- |
| `org.junit.jupiter:junit-jupiter` | `5.10.2` | `test` | JUnit 5 テスティングフレームワーク（JDK 8 対応版） |
| `org.springframework:spring-test` | `5.3.39` | `test` | Spring TestContext Framework (MockMvc, @WebAppConfiguration) |
| `org.mockito:mockito-junit-jupiter` | `4.11.0` | `test` | モックフレームワーク（Mockito 5 以降は Java 11 必須のため 4 系を採用） |
| `org.hamcrest:hamcrest` | `2.2` | `test` | MockMvc アサーション用マッチャー (`hasSize` 等) |

### ビルドプラグイン

| プラグイン名 | バージョン | 役割 / 設定 |
| :--- | :--- | :--- |
| `maven-war-plugin` | `3.3.2` | WAR アーカイブ生成（`failOnMissingWebXml: false` により Java Config に対応） |

---

## 3. プロジェクト構成

```text
spring-mvc-jdk8-sample/
├── pom.xml
├── README.md
└── src/
    ├── main/
    │   ├── java/
    │   │   └── com/
    │   │       └── example/
    │   │           ├── config/
    │   │           │   ├── AppInitializer.java     # DispatcherServlet 登録 (web.xml 代替)
    │   │           │   └── WebConfig.java          # ViewResolver・コンポーネントスキャン設定
    │   │           ├── controller/
    │   │           │   └── ItemController.java     # コントローラ (@Controller)
    │   │           └── model/
    │   │               └── Item.java               # データモデル (JavaBeans)
    │   └── webapp/
    │       └── WEB-INF/
    │           └── views/
    │               └── items.jsp                   # ビュー (JSP + JSTL)
    └── test/
        └── java/
            └── com/
                └── example/
                    └── controller/
                        └── ItemControllerTest.java # SpringExtension + MockMvc テスト
```

---

## 4. Maven コマンド実行例

**重要:** すべてのコマンドは `pom.xml` が配置されているプロジェクトのルートディレクトリで実行してください。

### 全テストの実行
```bash
mvn clean test
```

### 特定のテストクラスのみ実行
```bash
mvn test -Dtest=ItemControllerTest
```

### WAR ファイルのビルド（パッケージング）
テストを実行した上で、`target/spring-mvc-jdk8-sample.war` を生成します。
```bash
mvn clean package
```

### テストをスキップして WAR を生成
```bash
mvn clean package -DskipTests
```

### 依存関係ツリーの表示
プロジェクトに解決されている全ライブラリの階層構造を確認します。
```bash
mvn dependency:tree
```

### ビルド成果物の削除
```bash
mvn clean
```

---

## 5. デプロイと動作確認手順

Spring Boot と異なり組み込みサーバーは内包されていないため、外部の Tomcat を使用します。

1. **WAR の作成**
   ```bash
   mvn clean package
   ```
2. **Tomcat への配置**
   生成された `target/spring-mvc-jdk8-sample.war` を、Tomcat 8.5 または 9.0 の `webapps/` ディレクトリにコピーします。
3. **Tomcat の起動**
   Tomcat の `bin/startup.sh`（Windows は `bin/startup.bat`）を実行します。
4. **ブラウザでのアクセス**
   ```text
   http://localhost:8080/spring-mvc-jdk8-sample/items
   ```
5. **動作検証**
   * 初期データ（2件）が表示されることを確認します。
   * 入力フォームにテキストを入力して「追加」ボタンを押下し、一覧に追加されることを確認します。

---

## 6. 開発時の留意点・トラブルシューティング

### ① テスト実行時に `AssertionError: Expected: a collection with size <2> but: collection size was <3>` が出る
* **原因:** Spring のテストコンテキストがキャッシュされ、テストメソッド間でコントローラ内のリスト状態が汚染されている（POST テストが先に走り、データが増加した）ことが原因です。
* **対処法:** `ItemControllerTest` に `@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)` を付与し、テストメソッドごとにコンテキストをリフレッシュしてください。

### ② `The import org.hamcrest.Matchers cannot be resolved` が発生する
* **原因:** Spring Boot と異なり、Spring Framework 単体構成では Hamcrest が自動で依存関係に含まれません。
* **対処法:** `pom.xml` に `org.hamcrest:hamcrest:2.2` を追加してください。

### ③ セキュリティおよびサポートに関する留意点（サプライチェーンリスク）
* `Spring Framework 5.3.x` 系列は 2024 年 8 月をもってオープンソース（コミュニティ）サポートが終了（EOL）しています。
* 無償利用を継続する場合、EOL 後に報告された脆弱性（例: CVE-2024-38816, CVE-2024-38819 などのパストラバーサル）に対する公式パッチが Maven Central に提供されません。
* 本番稼働させる場合は、商用サポートの契約、WAF等による外部防御、または **Java 17/21 + Spring Framework 6.x** へのモダナイゼーションを検討してください。