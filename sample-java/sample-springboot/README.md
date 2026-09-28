# Spring Boot + JSP サンプルアプリケーション (JDK 8)

Spring Boot 2.7 (Spring MVC) をコントローラ、JSP (JSTL 1.2) をビュー、JavaBeans をモデルとしたメモ管理 Web アプリケーションです。
本プロジェクトは **Java 8 (JDK 8)** および **Java EE (javax.* 名前空間)*\* を前提に設計されています。

## 1. 動作環境要件

* **Java (JDK):** 1.8 (Java 8)

* **ビルドツール:** Apache Maven 3.6 以上

* **フレームワーク:** Spring Boot 2.7.18（JDK 8 に対応する最終マイナーバージョン系列）

* **実行環境:** 組み込み Apache Tomcat（Spring Boot 内包）または外部サーブレットコンテナ

## 2. 依存パッケージおよびプラグイン一覧

### 親 POM (BOM)

| グループID / アーティファクトID | バージョン | 役割 | 
 | ----- | ----- | ----- | 
| `org.springframework.boot:spring-boot-starter-parent` | `2.7.18` | 依存ライブラリのバージョン管理および標準ビルド定義 | 

### アプリケーション / テスト依存ライブラリ

| グループID / アーティファクトID | バージョン | スコープ | 用途 / 備考 | 
 | ----- | ----- | ----- | ----- | 
| `org.springframework.boot:spring-boot-starter-web` | `2.7.18` (Parent管理) | `compile` | Spring MVC、REST、組み込み Tomcat | 
| `org.apache.tomcat.embed:tomcat-embed-jasper` | `9.0.83` (Parent管理) | `provided` | 組み込み Tomcat で JSP をコンパイル・描画するために必須 | 
| `javax.servlet:jstl` | `1.2` (Parent管理) | `compile` | JSP 標準タグライブラリ (JSTL) | 
| `org.springframework.boot:spring-boot-starter-test` | `2.7.18` (Parent管理) | `test` | JUnit 5, Mockito, AssertJ, MockMvc 等のテスト群 | 

### ビルドプラグイン

| プラグイン名 | 役割 | 
 | ----- | ----- | 
| `spring-boot-maven-plugin` | 実行可能アーカイブの作成および `mvn spring-boot:run` による起動サポート | 

## 3. プロジェクト構成

JSP ファイルを組み込み Tomcat で認識させるため、`src/main/webapp` 配下にビューを配置し、`<packaging>war</packaging>` を指定しています。

```
spring-boot-jsp-jdk8/
├── pom.xml
├── README.md
└── src/
    ├── main/
    │   ├── java/
    │   │   └── com/
    │   │       └── example/
    │   │           ├── Application.java          # Spring Boot 起動クラス
    │   │           ├── controller/
    │   │           │   └── ItemController.java   # コントローラ (@Controller)
    │   │           └── model/
    │   │               └── Item.java             # データモデル (JavaBeans)
    │   ├── resources/
    │   │   └── application.properties            # ViewResolver等の設定
    │   └── webapp/
    │       └── WEB-INF/
    │           └── views/
    │               └── items.jsp                 # ビュー (JSP + JSTL)
    └── test/
        └── java/
            └── com/
                └── example/
                    └── controller/
                        └── ItemControllerTest.java # WebMvcTest (MockMvc)

```

## 4. Maven コマンド実行例

**注意:** すべてのコマンドは `pom.xml` が配置されている **プロジェクトのルートディレクトリ** で実行してください。

### アプリケーションのローカル起動

組み込み Tomcat を立ち上げて即座に動作確認を行います。

```
mvn spring-boot:run

```

### 全テストの実行

```
mvn test

```

### 特定のテストクラスのみ実行

```
mvn test -Dtest=ItemControllerTest

```

### WAR ファイルのビルド（パッケージング）

テストを実行し、外部 Tomcat 配置または単体起動が可能な WAR ファイルを `target/` 配下に生成します。

```
mvn clean package

```

### テストをスキップしてビルド

```
mvn clean package -DskipTests

```

### 生成物のクリーン（ビルド成果物の破棄）

```
mvn clean

```

## 5. 動作確認

1. **アプリ起動**

   プロジェクトルートで以下のコマンドを実行します。

   ```
   mvn spring-boot:run
   
   ```

2. **ブラウザでのアクセス**

   ブラウザから以下の URL にアクセスします。

   ```
   http://localhost:8080/items
   
   ```

3. **動作テスト**

   テキストボックスに任意の名称を入力して「追加」ボタンを押下し、一覧に追加されることを確認します。

## 6. トラブルシューティング

### Q1. `MissingProjectException: The goal you specified requires a project to execute but there is no POM in this directory` が発生する

* **原因:** コマンドの実行場所が `src` ディレクトリなどのサブフォルダになっています。

* **対処法:** `cd ..` で `pom.xml` が存在するルートディレクトリに戻ってからコマンドを再実行してください。

### Q2. 画面にアクセスすると JSP のソースコードがそのまま表示される / 404 エラーになる

* **原因:** `tomcat-embed-jasper` が依存関係に含まれていないか、スコープが不適切です。

* **対処法:** `pom.xml` に `org.apache.tomcat.embed:tomcat-embed-jasper` が定義されていることを確認してください。