<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="ja" sourcelanguage="zh_CN">
    <context>
        <name>RecoBox</name>
        <message>
            <location filename="../network.py" line="16" />
            <source>代理地址必须是主机:端口或 HTTP/HTTPS 地址</source>
            <translation>プロキシは ホスト:ポート または HTTP/HTTPS URL で指定してください</translation>
        </message>
        <message>
            <location filename="../network.py" line="18" />
            <source>代理地址不能包含账号密码</source>
            <translation>プロキシにユーザー名やパスワードは含められません</translation>
        </message>
        <message>
            <location filename="../network.py" line="20" />
            <source>代理地址不能包含路径、查询参数或片段</source>
            <translation>プロキシにパス、クエリ、フラグメントは含められません</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="200" />
            <source>仍有直播间正在录制或转换，请先全部暂停并等待收尾完成</source>
            <translation>録画または変換中のルームがあります。すべて一時停止して完了を待ってください</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="274" />
            <source>找不到直播间</source>
            <translation>ルームが見つかりません</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="277" />
            <source>直播间地址不能为空</source>
            <translation>ルーム URL は空にできません</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="280" />
            <source>该直播间地址已经存在</source>
            <translation>このルーム URL は既に存在します</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="283" />
            <source>保存目录不能为空</source>
            <translation>保存先は空にできません</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="291" />
            <source>检测间隔必须是正整数</source>
            <translation>確認間隔は正の整数で指定してください</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="293" />
            <source>检测间隔不能低于 30 秒</source>
            <translation>確認間隔は 30 秒未満にできません</translation>
        </message>
        <message>
            <location filename="../ffmpeg.py" line="28" />
            <location filename="../room_model.py" line="299" />
            <location filename="../room_model.py" line="301" />
            <location filename="../view_models.py" line="200" />
            <source>分段分钟数必须是正整数</source>
            <translation>分割時間は正の整数で指定してください</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="305" />
            <source>不支持该输出格式</source>
            <translation>未対応の出力形式です</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="187" />
            <source>默认录制目录不能为空</source>
            <translation>既定の録画先は空にできません</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="198" />
            <source>轮询间隔不能低于 30 秒</source>
            <translation>ポーリング間隔は 30 秒未満にできません</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="202" />
            <source>磁盘保护阈值必须是 1 至 1024 GB</source>
            <translation>ディスク保護しきい値は 1～1024 GB です</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="243" />
            <source>设置保存后校验失败，请重试</source>
            <translation>保存後の設定検証に失敗しました。再試行してください</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="288" />
            <source>选择文件夹</source>
            <translation>フォルダーを選択</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="356" />
            <source>预检失败：{error}</source>
            <translation>事前確認に失敗：{error}</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="372" />
            <source>导入失败：{error}</source>
            <translation>インポートに失敗：{error}</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="94" />
            <source>找不到已锁定的解析源码：{path}</source>
            <translation>固定リゾルバーのソースが見つかりません：{path}</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="133" />
            <source>暂不支持该直播间链接</source>
            <translation>このライブ URL はまだ対応していません</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="165" />
            <source>当前锁定版淘宝解析器要求登录会话，Reco Box 不导入账号或 Cookie，因此暂不尝试绕过；后续需要实现匿名公开接口后才能启用。</source>
            <translation>固定された Taobao リゾルバーはログイン済みセッションを要求します。Reco Box はアカウントや Cookie を取り込まず制限も回避しません。公開匿名 API の実装後に有効化できます。</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="212" />
            <source>该 TwitCasting 直播间要求登录，匿名模式不可用</source>
            <translation>この TwitCasting ルームはログインが必要なため匿名モードを使用できません</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="219" />
            <source>该 TwitCasting 页面无法匿名读取，可能需要登录或已受访问限制</source>
            <translation>この TwitCasting ページは匿名で読めません。ログインまたはアクセス制限の可能性があります</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="243" />
            <source>TwitCasting 未返回可录制的公开播放地址</source>
            <translation>TwitCasting から録画可能な公開 URL が返されませんでした</translation>
        </message>
        <message>
            <location filename="../recording.py" line="206" />
            <source>未找到 FFmpeg；开发版需要设置 RECO_BOX_FFMPEG</source>
            <translation>FFmpeg が見つかりません。開発版では RECO_BOX_FFMPEG を設定してください</translation>
        </message>
        <message>
            <location filename="../recording.py" line="236" />
            <source>磁盘剩余空间低于 {minimum_free_gb:g} GB，已阻止开始录制</source>
            <translation>空き容量が {minimum_free_gb:g} GB 未満のため録画を開始しません</translation>
        </message>
        <message>
            <location filename="../recording.py" line="330" />
            <source>未找到可用直播线路</source>
            <translation>利用可能な配信ルートが見つかりません</translation>
        </message>
        <message>
            <location filename="../recording.py" line="487" />
            <source>未找到 ffprobe</source>
            <translation>ffprobe が見つかりません</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="95" />
            <location filename="../recording.py" line="492" />
            <source>录制目录中没有媒体文件</source>
            <translation>録画フォルダーにメディアファイルがありません</translation>
        </message>
        <message>
            <location filename="../preview.py" line="16" />
            <location filename="../preview.py" line="36" />
            <location filename="../preview.py" line="41" />
            <source>直播预览</source>
            <translation>ライブプレビュー</translation>
        </message>
        <message>
            <location filename="../preview.py" line="37" />
            <source>尚未取得直播流，请先点击“立即检查并录制”</source>
            <translation>配信を取得していません。先に「今すぐ確認して録画」を押してください</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="85" />
            <source>ffprobe 验证失败</source>
            <translation>ffprobe 検証に失敗</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="89" />
            <source>ffprobe 返回了无效 JSON</source>
            <translation>ffprobe が無効な JSON を返しました</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="112" />
            <source>文件中没有可识别的音视频流</source>
            <translation>認識可能な音声・映像ストリームがありません</translation>
        </message>
        <message>
            <location filename="../ffmpeg.py" line="26" />
            <source>必须先设置录制保存目录</source>
            <translation>先に録画保存先を設定してください</translation>
        </message>
        <message>
            <location filename="../output_paths.py" line="46" />
            <location filename="../output_paths.py" line="53" />
            <source>输出格式必须是简单扩展名</source>
            <translation>出力形式は単純な拡張子で指定してください</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="418" />
            <source>Resolver 调度限制</source>
            <translation>Resolver スケジューリング制限</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="421" />
            <source>最大并发</source>
            <translation>最大同時実行数</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="422" />
            <source>单平台并发</source>
            <translation>プラットフォームごとの同時実行数</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="423" />
            <source>平台冷却（秒）</source>
            <translation>プラットフォームのクールダウン（秒）</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="425" />
            <source>用于分散解析请求；修改后立即影响新的监控请求。</source>
            <translation>Resolver リクエストを分散するために使用します。変更は新しい監視リクエストに直ちに適用されます。</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="196" />
            <source>轮询、分段和解析限制参数必须是整数</source>
            <translation>ポーリング、セグメント、Resolver 制限のパラメーターは整数である必要があります</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="204" />
            <source>Resolver 最大并发必须是 1 至 32</source>
            <translation>Resolver の最大同時実行数は 1～32 である必要があります</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="206" />
            <source>单平台并发必须是 1 至 16</source>
            <translation>プラットフォームごとの同時実行数は 1～16 である必要があります</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="208" />
            <source>平台冷却必须是 0 至 3600 秒</source>
            <translation>プラットフォームのクールダウンは 0～3600 秒である必要があります</translation>
        </message>
    </context>
    <context>
        <name>Main</name>
        <message>
            <location filename="../ui/Main.qml" line="35" />
            <source>全部状态</source>
            <translation>全ステータス</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="36" />
            <location filename="../ui/Main.qml" line="241" />
            <location filename="../ui/Main.qml" line="448" />
            <source>录制中</source>
            <translation>録音中</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="241" />
            <source>卡顿收尾</source>
            <translation>停止処理中</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="37" />
            <location filename="../ui/Main.qml" line="241" />
            <source>监控中</source>
            <translation>モニタリング</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="38" />
            <location filename="../ui/Main.qml" line="241" />
            <source>未开始</source>
            <translation>未開始</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="41" />
            <source>默认排序</source>
            <translation>デフォルトの並べ替え</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="42" />
            <source>名称正序</source>
            <translation>名前シーケンス</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="43" />
            <source>名称倒序</source>
            <translation>名前の逆順</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="46" />
            <source>原画</source>
            <translation>原画</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="47" />
            <source>蓝光</source>
            <translation>ブルーレイ</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="48" />
            <source>超清</source>
            <translation>ウルトラ HD</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="49" />
            <source>高清</source>
            <translation>HD</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="50" />
            <source>标清</source>
            <translation>SD</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="51" />
            <source>流畅</source>
            <translation>スムーズ</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="54" />
            <source>线路1</source>
            <translation>1行目</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="55" />
            <source>线路2</source>
            <translation>2行目</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="56" />
            <source>线路3</source>
            <translation>3行目</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="57" />
            <source>线路4</source>
            <translation>4行目</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="58" />
            <source>线路5</source>
            <translation>5行目</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="163" />
            <location filename="../ui/Main.qml" line="280" />
            <location filename="../ui/Main.qml" line="287" />
            <source>添加直播间</source>
            <translation>ライブブロードキャストルームを追加</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="166" />
            <source>一键全部开始录屏 / 监控</source>
            <translation>ワンクリックですべての録画/監視を開始</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="167" />
            <source>已启用全部直播间并立即检查</source>
            <translation>すべてのライブ ブロードキャスト ルームが有効になり、現在チェックされています</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="170" />
            <source>一键全部暂停录屏 / 监控</source>
            <translation>ワンクリックですべての画面の録画/監視を一時停止します</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="171" />
            <source>已请求全部暂停；正在录制的文件会先安全收尾</source>
            <translation>すべての一時停止が要求されました。記録中のファイルは最初に安全に終了します</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="173" />
            <location filename="../ui/Main.qml" line="370" />
            <source>删除全部直播间</source>
            <translation>すべてのライブ ブロードキャスト ルームを削除します</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="175" />
            <source>全局设置、录制历史和运行日志</source>
            <translation>グローバル設定、記録履歴および実行ログ</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="181" />
            <source>搜索主播、标题或链接…</source>
            <translation>アンカー、タイトル、リンクを検索…</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="189" />
            <source>直播间</source>
            <translation>ライブブロードキャストルーム</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="241" />
            <source>转 MP4</source>
            <translation>を MP4 に</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="241" />
            <source>检查中</source>
            <translation>チェック中</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="244" />
            <source>暂无直播间标题</source>
            <translation>ライブ ブロードキャスト ルームのタイトルはまだありません</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source>分段：</source>
            <translation>セグメンテーション:</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source>每 </source>
            <translation>毎</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source> 分钟</source>
            <translation>分</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source>关闭</source>
            <translation>閉じる</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source> · 完成后转 MP4</source>
            <translation>・完了後MP4に変換</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="250" />
            <source>检测间隔 </source>
            <translation>検出間隔</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="250" />
            <source> 秒</source>
            <translation>秒</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="254" />
            <source>错误：</source>
            <translation>エラー:</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="259" />
            <source>停止并暂停</source>
            <translation>停止して一時停止する</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="259" />
            <source>暂停监控</source>
            <translation>監視を一時停止します</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="259" />
            <source>开始监控</source>
            <translation>監視開始</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="264" />
            <source>检查并录制</source>
            <translation>確認と記録</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="268" />
            <source>预览</source>
            <translation>プレビュー</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="269" />
            <source>编辑</source>
            <translation>編集</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="271" />
            <source>删除</source>
            <translation>削除</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="278" />
            <source>还没有直播间</source>
            <translation>ライブ ブロードキャスト ルームはまだありません</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="278" />
            <source>没有符合当前筛选条件的直播间</source>
            <translation>現在のフィルター条件を満たすライブ ブロードキャスト ルームはありません</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="279" />
            <source>添加公开直播间地址后，Reco Box 会自动开始监控</source>
            <translation>公開ライブブロードキャストルームのアドレスを追加すると、Reco Boxは自動的に監視を開始します</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="279" />
            <source>调整状态筛选或搜索关键词后重试</source>
            <translation>ステータスフィルターを調整するか、キーワードを検索して再試行してください</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="290" />
            <source>直播间添加成功</source>
            <translation>ライブ ブロードキャスト ルームが正常に追加されました</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="293" />
            <location filename="../ui/Main.qml" line="322" />
            <source>直播间地址</source>
            <translation>ライブブロードキャストルームアドレス</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="294" />
            <source>粘贴公开直播间链接</source>
            <translation>公開ライブ ブロードキャスト ルームのリンクを貼り付けます</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="295" />
            <source>主播名字（可稍后自动识别）</source>
            <translation>アンカー名 (後で自動的に認識できます)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="296" />
            <source>待识别主播</source>
            <translation>アンカーを特定する</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="297" />
            <location filename="../ui/Main.qml" line="335" />
            <source>保存目录</source>
            <translation>保存ディレクトリ</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="298" />
            <location filename="../ui/Main.qml" line="336" />
            <location filename="../ui/Main.qml" line="410" />
            <source>选择目录</source>
            <translation>ディレクトリを選択</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="299" />
            <source>格式、画质、检测间隔和分段使用已保存的全局默认设置。</source>
            <translation>形式、品質、検出間隔、およびセグメンテーションは、保存されたグローバルなデフォルト設定を使用します。</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="306" />
            <source>编辑直播间</source>
            <translation>ライブ ブロードキャスト ルームを編集する</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="321" />
            <source>基础编辑</source>
            <translation>基本的な編集</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="324" />
            <source>主播名字</source>
            <translation>アンカー名</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="326" />
            <source>直播间标题</source>
            <translation>ライブブロードキャストルームのタイトル</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="327" />
            <source>可以留空，开播后自动更新</source>
            <translation>は空白のままにすることができ、放送後に自動的に更新されます。</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="329" />
            <source>录制设置</source>
            <translation>録画設定</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="332" />
            <source>文件名（不分段时使用）</source>
            <translation>ファイル名(分割されていない場合に使用)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="332" />
            <source>留空则使用 1</source>
            <translation>1を使用するには空白のままにしてください</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="333" />
            <location filename="../ui/Main.qml" line="415" />
            <source>检测间隔（秒）</source>
            <translation>検出間隔(秒)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="337" />
            <source>代理地址（可选）</source>
            <translation>プロキシ アドレス (オプション)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="338" />
            <source>例如 127.0.0.1:7890；留空表示直连</source>
            <translation>例: 127.0.0.1:7890;直接接続を示す場合は空白のままにします</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="341" />
            <source>录制清晰度</source>
            <translation>鮮明な録音</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="342" />
            <source>录制路线</source>
            <translation>録画ルート</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="346" />
            <source>输出格式</source>
            <translation>出力形式</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="347" />
            <source>分段时长（分钟）</source>
            <translation>セグメント期間 (分)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="347" />
            <source>启用</source>
            <translation>有効にする</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="349" />
            <source>分段文件固定按 1、2、3… 排列，最后一段按实际剩余时长保存。</source>
            <translation>セグメント化されたファイルは 1、2、3... に固定的に配置され、最後のセグメントは実際の残り時間に応じて保存されます。</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="350" />
            <source>录制完成后转为 MP4（成功后删除 TS）</source>
            <translation>録画完了後にMP4に変換（成功後はTSを削除）</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="351" />
            <source>纯音频模式</source>
            <translation>音声のみモード</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="352" />
            <source>录制弹幕（仅在平台适配完成后生效）</source>
            <translation>弾幕を記録します (プラットフォームの適応が完了した後にのみ有効になります)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="359" />
            <location filename="../ui/Main.qml" line="378" />
            <source>取消</source>
            <translation>キャンセル</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="361" />
            <source>保存</source>
            <translation>保存</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="362" />
            <source>直播间设置已保存</source>
            <translation>ライブブロードキャストルームの設定が保存されました</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="376" />
            <source>确定从 Reco Box 中删除全部直播间吗？
录制文件和历史记录不会删除。</source>
            <translation>すべてのライブ ブロードキャスト ルームをレコ ボックスから削除してもよろしいですか?
録画ファイルや履歴は削除されません。</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="378" />
            <source>确认全部删除</source>
            <translation>すべての削除を確認します</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="378" />
            <source>已删除全部直播间</source>
            <translation>すべてのライブ ブロードキャスト ルームが削除されました</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="384" />
            <location filename="../ui/Main.qml" line="389" />
            <source>全局设置</source>
            <translation>グローバル設定</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="389" />
            <source>录制历史</source>
            <translation>記録履歴</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="389" />
            <source>运行日志</source>
            <translation>実行ログ</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="396" />
            <source>新直播间默认设置</source>
            <translation>新しいライブ ブロードキャスト ルームのデフォルト設定</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="396" />
            <source>导入旧配置</source>
            <translation>古い構成をインポートする</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="397" />
            <source>界面语言</source>
            <translation>インターフェース言語</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="404" />
            <source>界面语言已切换</source>
            <translation>インターフェース言語が切り替えられました</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="408" />
            <source>只影响以后新增或导入的直播间；已有直播间在卡片中单独编辑。</source>
            <translation>は、将来追加またはインポートされるライブ ブロードキャスト ルームにのみ影響します。既存のライブ ブロードキャスト ルームはカード内で個別に編集できます。</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="409" />
            <source>默认录制目录</source>
            <translation>デフォルトの録音ディレクトリ</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="413" />
            <source>默认格式</source>
            <translation>デフォルトの形式</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="414" />
            <source>默认画质</source>
            <translation>デフォルトの品質</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="416" />
            <source>磁盘保护（GB）</source>
            <translation>ディスク保護 (GB)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="426" />
            <source>默认代理地址（可选）</source>
            <translation>デフォルトのプロキシ アドレス (オプション)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="427" />
            <source>新直播间继承；留空表示直连</source>
            <translation>新しいライブ ブロードキャスト ルームが継承されます。直接接続を示す場合は空白のままにします</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="428" />
            <source>新直播间默认启用分段</source>
            <translation>新しいライブ ブロードキャスト ルームではデフォルトでセグメンテーションが有効になります</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="428" />
            <location filename="../ui/Main.qml" line="429" />
            <source>设置已更改，请点击保存设置</source>
            <translation>設定が変更されました。クリックして設定を保存してください</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="429" />
            <source>每段</source>
            <translation>各段落</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="429" />
            <source>分钟，最后一段按实际时长保存</source>
            <translation>分、最後のセグメントは実際の長さに応じて保存されます</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="432" />
            <source>启动后自动监控 · 关闭窗口最小化到托盘 · 不随 Windows 开机启动</source>
            <translation>起動後自動的に監視する ・ウィンドウを閉じてトレイに最小化する ・Windowsの起動と同時に起動しない</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source>保存设置</source>
            <translation>設定の保存</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source>已保存并确认：以后新增直播间默认每 </source>
            <translation>保存および確認: 今後の各新しいライブ ブロードキャスト ルームのデフォルト</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source> 分钟分段</source>
            <translation>分のセグメント</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source>已保存并确认：以后新增直播间默认不分段</source>
            <translation>保存および確認: 今後、新しいライブ ブロードキャスト ルームはデフォルトでセグメント化されなくなります。</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="436" />
            <source>已保存并确认</source>
            <translation>保存して確認しました</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="436" />
            <source>设置已更改</source>
            <translation>設定が変更されました</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>可播放</source>
            <translation>再生可能</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>转 MP4 中</source>
            <translation>MP4 に変換</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>已完成</source>
            <translation>完了</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>失败</source>
            <translation>が失敗しました</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="449" />
            <location filename="../ui/Main.qml" line="514" />
            <source>播放</source>
            <translation>プレイ</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="450" />
            <source>目录</source>
            <translation>ディレクトリ</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="455" />
            <source>这里只显示脱敏后的状态和错误，不保存完整临时播放地址。</source>
            <translation>ここでは、感度解除後のステータスとエラーのみが表示され、完全な一時再生アドレスは保存されません。</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="480" />
            <source>直播流播放失败</source>
            <translation>ライブ ストリームの再生に失敗しました</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="484" />
            <source>直播流格式无效或播放器无法解码</source>
            <translation>ライブ ストリームの形式が無効であるか、プレーヤーがそれをデコードできません</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="508" />
            <source>正在准备预览……</source>
            <translation>プレビューの準備中...</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="509" />
            <source>正在连接直播流并等待首帧……</source>
            <translation>ライブ ストリームに接続し、最初のフレームを待機しています...</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="514" />
            <source>暂停</source>
            <translation>一時停止</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="514" />
            <source>静音</source>
            <translation>ミュート</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="520" />
            <source>导入 DouyinLiveRecorder 旧配置</source>
            <translation>DouyinLiveRecorder の古い設定をインポートします</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="524" />
            <source>选择旧程序根目录或其中的 config 文件夹。</source>
            <translation>古いプログラムのルート ディレクトリまたはその中の config フォルダーを選択します。</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="525" />
            <source>选择文件夹</source>
            <translation>フォルダを選択</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="526" />
            <source>1. 预检</source>
            <translation>1．事前チェック</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="526" />
            <source>2. 确认导入</source>
            <translation>2．インポートの確認</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="526" />
            <source>可导入直播间</source>
            <translation>はライブブロードキャストルームにインポートできます</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="528" />
            <source>不会修改旧配置；Cookie、令牌、账号、密码和推送凭据不会导入。</source>
            <translation>古い構成は変更されません。 Cookie、トークン、アカウント、パスワード、およびプッシュ認証情報はインポートされません。</translation>
        </message>
    </context>
</TS>
