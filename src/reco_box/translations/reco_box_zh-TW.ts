<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="zh-TW" sourcelanguage="zh_CN">
    <context>
        <name>RecoBox</name>
        <message>
            <location filename="../network.py" line="16" />
            <source>代理地址必须是主机:端口或 HTTP/HTTPS 地址</source>
            <translation>代理位址必須是主機:連接埠或 HTTP/HTTPS 位址</translation>
        </message>
        <message>
            <location filename="../network.py" line="18" />
            <source>代理地址不能包含账号密码</source>
            <translation>代理位址不能包含帳號密碼</translation>
        </message>
        <message>
            <location filename="../network.py" line="20" />
            <source>代理地址不能包含路径、查询参数或片段</source>
            <translation>代理位址不能包含路徑、查詢參數或片段</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="200" />
            <source>仍有直播间正在录制或转换，请先全部暂停并等待收尾完成</source>
            <translation>仍有直播間正在錄製或轉換，請先全部暫停並等待收尾完成</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="274" />
            <source>找不到直播间</source>
            <translation>找不到直播間</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="277" />
            <source>直播间地址不能为空</source>
            <translation>直播間位址不能為空</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="280" />
            <source>该直播间地址已经存在</source>
            <translation>該直播間位址已經存在</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="283" />
            <source>保存目录不能为空</source>
            <translation>儲存目錄不能為空</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="291" />
            <source>检测间隔必须是正整数</source>
            <translation>偵測間隔必須是正整數</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="293" />
            <source>检测间隔不能低于 30 秒</source>
            <translation>偵測間隔不能低於 30 秒</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="299" />
            <location filename="../room_model.py" line="301" />
            <location filename="../view_models.py" line="173" />
            <location filename="../ffmpeg.py" line="28" />
            <source>分段分钟数必须是正整数</source>
            <translation>分段分鐘數必須是正整數</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="305" />
            <source>不支持该输出格式</source>
            <translation>不支援該輸出格式</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="163" />
            <source>默认录制目录不能为空</source>
            <translation>預設錄製目錄不能為空</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="169" />
            <source>轮询秒数和分段分钟数必须是正整数</source>
            <translation>輪詢秒數和分段分鐘數必須是正整數</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="171" />
            <source>轮询间隔不能低于 30 秒</source>
            <translation>輪詢間隔不能低於 30 秒</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="175" />
            <source>磁盘保护阈值必须是 1 至 1024 GB</source>
            <translation>磁碟保護門檻必須是 1 至 1024 GB</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="200" />
            <source>设置保存后校验失败，请重试</source>
            <translation>設定儲存後驗證失敗，請重試</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="236" />
            <source>选择文件夹</source>
            <translation>選擇資料夾</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="304" />
            <source>预检失败：{error}</source>
            <translation>預檢失敗：{error}</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="320" />
            <source>导入失败：{error}</source>
            <translation>匯入失敗：{error}</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="81" />
            <source>找不到已锁定的解析源码：{path}</source>
            <translation>找不到已鎖定的解析原始碼：{path}</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="120" />
            <source>暂不支持该直播间链接</source>
            <translation>暫不支援該直播間連結</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="149" />
            <source>当前锁定版淘宝解析器要求登录会话，Reco Box 不导入账号或 Cookie，因此暂不尝试绕过；后续需要实现匿名公开接口后才能启用。</source>
            <translation>目前鎖定版淘寶解析器要求登入工作階段，Reco Box 不匯入帳號或 Cookie，因此不嘗試繞過；實作匿名公開介面後才能啟用。</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="196" />
            <source>该 TwitCasting 直播间要求登录，匿名模式不可用</source>
            <translation>該 TwitCasting 直播間要求登入，匿名模式不可用</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="203" />
            <source>该 TwitCasting 页面无法匿名读取，可能需要登录或已受访问限制</source>
            <translation>該 TwitCasting 頁面無法匿名讀取，可能需要登入或已受存取限制</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="226" />
            <source>TwitCasting 未返回可录制的公开播放地址</source>
            <translation>TwitCasting 未傳回可錄製的公開播放位址</translation>
        </message>
        <message>
            <location filename="../recording.py" line="206" />
            <source>未找到 FFmpeg；开发版需要设置 RECO_BOX_FFMPEG</source>
            <translation>找不到 FFmpeg；開發版需要設定 RECO_BOX_FFMPEG</translation>
        </message>
        <message>
            <location filename="../recording.py" line="236" />
            <source>磁盘剩余空间低于 {minimum_free_gb:g} GB，已阻止开始录制</source>
            <translation>磁碟剩餘空間低於 {minimum_free_gb:g} GB，已阻止開始錄製</translation>
        </message>
        <message>
            <location filename="../recording.py" line="330" />
            <source>未找到可用直播线路</source>
            <translation>找不到可用直播線路</translation>
        </message>
        <message>
            <location filename="../recording.py" line="487" />
            <source>未找到 ffprobe</source>
            <translation>找不到 ffprobe</translation>
        </message>
        <message>
            <location filename="../recording.py" line="492" />
            <location filename="../media_probe.py" line="95" />
            <source>录制目录中没有媒体文件</source>
            <translation>錄製目錄中沒有媒體檔案</translation>
        </message>
        <message>
            <location filename="../preview.py" line="16" />
            <location filename="../preview.py" line="36" />
            <location filename="../preview.py" line="41" />
            <source>直播预览</source>
            <translation>直播預覽</translation>
        </message>
        <message>
            <location filename="../preview.py" line="37" />
            <source>尚未取得直播流，请先点击“立即检查并录制”</source>
            <translation>尚未取得直播串流，請先點擊「立即檢查並錄製」</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="85" />
            <source>ffprobe 验证失败</source>
            <translation>ffprobe 驗證失敗</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="89" />
            <source>ffprobe 返回了无效 JSON</source>
            <translation>ffprobe 傳回無效 JSON</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="112" />
            <source>文件中没有可识别的音视频流</source>
            <translation>檔案中沒有可識別的音訊或視訊串流</translation>
        </message>
        <message>
            <location filename="../ffmpeg.py" line="26" />
            <source>必须先设置录制保存目录</source>
            <translation>必須先設定錄製儲存目錄</translation>
        </message>
        <message>
            <location filename="../output_paths.py" line="46" />
            <location filename="../output_paths.py" line="53" />
            <source>输出格式必须是简单扩展名</source>
            <translation>輸出格式必須是簡單副檔名</translation>
        </message>
    </context>
    <context>
        <name>Main</name>
        <message>
            <location filename="../ui/Main.qml" line="35" />
            <source>全部状态</source>
            <translation>全部狀態</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="36" />
            <location filename="../ui/Main.qml" line="240" />
            <location filename="../ui/Main.qml" line="439" />
            <source>录制中</source>
            <translation>錄製中</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="37" />
            <location filename="../ui/Main.qml" line="240" />
            <source>监控中</source>
            <translation>監控中</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="38" />
            <location filename="../ui/Main.qml" line="240" />
            <source>未开始</source>
            <translation>未開始</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="41" />
            <source>默认排序</source>
            <translation>預設排序</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="42" />
            <source>名称正序</source>
            <translation>名稱正序</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="43" />
            <source>名称倒序</source>
            <translation>名稱倒序</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="46" />
            <source>原画</source>
            <translation>原畫</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="47" />
            <source>蓝光</source>
            <translation>藍光</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="48" />
            <source>超清</source>
            <translation>超清</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="49" />
            <source>高清</source>
            <translation>高清</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="50" />
            <source>标清</source>
            <translation>標清</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="51" />
            <source>流畅</source>
            <translation>流暢</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="54" />
            <source>线路1</source>
            <translation>線路1</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="55" />
            <source>线路2</source>
            <translation>線路2</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="56" />
            <source>线路3</source>
            <translation>線路3</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="57" />
            <source>线路4</source>
            <translation>線路4</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="58" />
            <source>线路5</source>
            <translation>線路5</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="162" />
            <location filename="../ui/Main.qml" line="279" />
            <location filename="../ui/Main.qml" line="286" />
            <source>添加直播间</source>
            <translation>新增直播間</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="165" />
            <source>一键全部开始录屏 / 监控</source>
            <translation>一鍵全部開始錄影 / 監控</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="166" />
            <source>已启用全部直播间并立即检查</source>
            <translation>已啟用全部直播間並立即檢查</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="169" />
            <source>一键全部暂停录屏 / 监控</source>
            <translation>一鍵全部暫停錄影畫面 / 監控</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="170" />
            <source>已请求全部暂停；正在录制的文件会先安全收尾</source>
            <translation>已要求全部暫停；正在錄製的檔案會先安全收尾</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="172" />
            <location filename="../ui/Main.qml" line="369" />
            <source>删除全部直播间</source>
            <translation>刪除全部直播間</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="174" />
            <source>全局设置、录制历史和运行日志</source>
            <translation>全域設定、錄製歷史和運行日誌</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="180" />
            <source>搜索主播、标题或链接…</source>
            <translation>搜尋主播、標題或連結…</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="188" />
            <source>直播间</source>
            <translation>直播間</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="240" />
            <source>转 MP4</source>
            <translation>轉 MP4</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="240" />
            <source>检查中</source>
            <translation>檢查中</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="243" />
            <source>暂无直播间标题</source>
            <translation>暫時沒有直播標題</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="244" />
            <source>分段：</source>
            <translation>分段：</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="244" />
            <source>每 </source>
            <translation>每</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="244" />
            <source> 分钟</source>
            <translation>分鐘</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="244" />
            <source>关闭</source>
            <translation>關閉</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="244" />
            <source> · 完成后转 MP4</source>
            <translation>· 完成後轉 MP4</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="249" />
            <source>检测间隔 </source>
            <translation>偵測間隔</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="249" />
            <source> 秒</source>
            <translation>秒</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="253" />
            <source>错误：</source>
            <translation>錯誤：</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="258" />
            <source>停止并暂停</source>
            <translation>停止並暫停</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="258" />
            <source>暂停监控</source>
            <translation>暫停監控</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="258" />
            <source>开始监控</source>
            <translation>開始監控</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="263" />
            <source>检查并录制</source>
            <translation>檢查並錄製</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="267" />
            <source>预览</source>
            <translation>預覽</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="268" />
            <source>编辑</source>
            <translation>編輯</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="270" />
            <source>删除</source>
            <translation>刪除</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="277" />
            <source>还没有直播间</source>
            <translation>還沒有直播間</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="277" />
            <source>没有符合当前筛选条件的直播间</source>
            <translation>沒有符合目前篩選條件的直播間</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="278" />
            <source>添加公开直播间地址后，Reco Box 会自动开始监控</source>
            <translation>新增公開直播間地址後，Reco Box 會自動開始監控</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="278" />
            <source>调整状态筛选或搜索关键词后重试</source>
            <translation>調整狀態篩選或搜尋關鍵字後重試</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="289" />
            <source>直播间添加成功</source>
            <translation>直播間新增成功</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="292" />
            <location filename="../ui/Main.qml" line="321" />
            <source>直播间地址</source>
            <translation>直播間地址</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="293" />
            <source>粘贴公开直播间链接</source>
            <translation>貼上公開直播間鏈接</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="294" />
            <source>主播名字（可稍后自动识别）</source>
            <translation>主播名字（可稍後自動辨識）</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="295" />
            <source>待识别主播</source>
            <translation>待辨識主播</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="296" />
            <location filename="../ui/Main.qml" line="334" />
            <source>保存目录</source>
            <translation>保存目錄</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="297" />
            <location filename="../ui/Main.qml" line="335" />
            <location filename="../ui/Main.qml" line="409" />
            <source>选择目录</source>
            <translation>選擇目錄</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="298" />
            <source>格式、画质、检测间隔和分段使用已保存的全局默认设置。</source>
            <translation>格式、畫質、偵測間隔和分段使用已儲存的全域預設設定。</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="305" />
            <source>编辑直播间</source>
            <translation>編輯直播間</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="320" />
            <source>基础编辑</source>
            <translation>基礎編輯</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="323" />
            <source>主播名字</source>
            <translation>主播名字</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="325" />
            <source>直播间标题</source>
            <translation>直播間標題</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="326" />
            <source>可以留空，开播后自动更新</source>
            <translation>可以留空，開播後自動更新</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="328" />
            <source>录制设置</source>
            <translation>錄製設定</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="331" />
            <source>文件名（不分段时使用）</source>
            <translation>檔名（不分段時使用）</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="331" />
            <source>留空则使用 1</source>
            <translation>留空則使用 1</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="332" />
            <location filename="../ui/Main.qml" line="414" />
            <source>检测间隔（秒）</source>
            <translation>偵測間隔（秒）</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="336" />
            <source>代理地址（可选）</source>
            <translation>代理位址（可選）</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="337" />
            <source>例如 127.0.0.1:7890；留空表示直连</source>
            <translation>例如 127.0.0.1:7890；留空表示直連</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="340" />
            <source>录制清晰度</source>
            <translation>錄製清晰度</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="341" />
            <source>录制路线</source>
            <translation>錄影路線</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="345" />
            <source>输出格式</source>
            <translation>輸出格式</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="346" />
            <source>分段时长（分钟）</source>
            <translation>分段時間（分鐘）</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="346" />
            <source>启用</source>
            <translation>啟用</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="348" />
            <source>分段文件固定按 1、2、3… 排列，最后一段按实际剩余时长保存。</source>
            <translation>分段檔案固定以 1、2、3… 排列，最後一段依實際剩餘時長儲存。</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="349" />
            <source>录制完成后转为 MP4（成功后删除 TS）</source>
            <translation>錄製完成後轉為 MP4（成功後刪除 TS）</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="350" />
            <source>纯音频模式</source>
            <translation>純音訊模式</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="351" />
            <source>录制弹幕（仅在平台适配完成后生效）</source>
            <translation>錄製彈幕（僅在平台適配完成後生效）</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="358" />
            <location filename="../ui/Main.qml" line="377" />
            <source>取消</source>
            <translation>取消</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="360" />
            <source>保存</source>
            <translation>保存</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="361" />
            <source>直播间设置已保存</source>
            <translation>直播間設定已儲存</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="375" />
            <source>确定从 Reco Box 中删除全部直播间吗？
录制文件和历史记录不会删除。</source>
            <translation>確定從 Reco Box 中刪除全部直播間嗎？
錄製檔案和歷史記錄不會刪除。</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="377" />
            <source>确认全部删除</source>
            <translation>確認全部刪除</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="377" />
            <source>已删除全部直播间</source>
            <translation>已刪除全部直播間</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="383" />
            <location filename="../ui/Main.qml" line="388" />
            <source>全局设置</source>
            <translation>全域設定</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="388" />
            <source>录制历史</source>
            <translation>錄製歷史</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="388" />
            <source>运行日志</source>
            <translation>運行日誌</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="395" />
            <source>新直播间默认设置</source>
            <translation>新直播間預設設定</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="395" />
            <source>导入旧配置</source>
            <translation>導入舊配置</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="396" />
            <source>界面语言</source>
            <translation>介面語言</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="403" />
            <source>界面语言已切换</source>
            <translation>介面語言已切換</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="407" />
            <source>只影响以后新增或导入的直播间；已有直播间在卡片中单独编辑。</source>
            <translation>只影響日後新增或匯入的直播間；已有直播間在卡片中單獨編輯。</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="408" />
            <source>默认录制目录</source>
            <translation>預設錄製目錄</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="412" />
            <source>默认格式</source>
            <translation>預設格式</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="413" />
            <source>默认画质</source>
            <translation>預設畫質</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="415" />
            <source>磁盘保护（GB）</source>
            <translation>磁碟保護（GB）</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="417" />
            <source>默认代理地址（可选）</source>
            <translation>預設代理位址（可選）</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="418" />
            <source>新直播间继承；留空表示直连</source>
            <translation>新直播間繼承；留空表示直連</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="419" />
            <source>新直播间默认启用分段</source>
            <translation>新直播間預設啟用分段</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="419" />
            <location filename="../ui/Main.qml" line="420" />
            <source>设置已更改，请点击保存设置</source>
            <translation>設定已更改，請點選儲存設定</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="420" />
            <source>每段</source>
            <translation>每段</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="420" />
            <source>分钟，最后一段按实际时长保存</source>
            <translation>分鐘，最後一段依實際時長保存</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="423" />
            <source>启动后自动监控 · 关闭窗口最小化到托盘 · 不随 Windows 开机启动</source>
            <translation>啟動後自動監控 · 關閉視窗最小化到托盤 · 不隨 Windows 開機啟動</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="425" />
            <source>保存设置</source>
            <translation>儲存設定</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="425" />
            <source>已保存并确认：以后新增直播间默认每 </source>
            <translation>已儲存並確認：以後新增直播間預設每</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="425" />
            <source> 分钟分段</source>
            <translation>分鐘分段</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="425" />
            <source>已保存并确认：以后新增直播间默认不分段</source>
            <translation>已儲存並確認：以後新增直播間預設不分段</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="427" />
            <source>已保存并确认</source>
            <translation>已儲存並確認</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="427" />
            <source>设置已更改</source>
            <translation>設定已更改</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="439" />
            <source>可播放</source>
            <translation>可播放</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="439" />
            <source>转 MP4 中</source>
            <translation>轉 MP4 中</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="439" />
            <source>已完成</source>
            <translation>已完成</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="439" />
            <source>失败</source>
            <translation>失敗</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="440" />
            <location filename="../ui/Main.qml" line="505" />
            <source>播放</source>
            <translation>播放</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="441" />
            <source>目录</source>
            <translation>目錄</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="446" />
            <source>这里只显示脱敏后的状态和错误，不保存完整临时播放地址。</source>
            <translation>這裡只顯示脫敏後的狀態和錯誤，不儲存完整臨時播放位址。</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="471" />
            <source>直播流播放失败</source>
            <translation>直播串流播放失敗</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="475" />
            <source>直播流格式无效或播放器无法解码</source>
            <translation>直播串流格式無效或播放器無法解碼</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="499" />
            <source>正在准备预览……</source>
            <translation>正在準備預覽…</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="500" />
            <source>正在连接直播流并等待首帧……</source>
            <translation>正在連接直播串流並等待首幀…</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="505" />
            <source>暂停</source>
            <translation>暫停</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="505" />
            <source>静音</source>
            <translation>靜音</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="511" />
            <source>导入 DouyinLiveRecorder 旧配置</source>
            <translation>導入 DouyinLiveRecorder 舊配置</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="515" />
            <source>选择旧程序根目录或其中的 config 文件夹。</source>
            <translation>選擇舊程式根目錄或其中的 config 資料夾。</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="516" />
            <source>选择文件夹</source>
            <translation>選擇資料夾</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="517" />
            <source>1. 预检</source>
            <translation>1. 預檢</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="517" />
            <source>2. 确认导入</source>
            <translation>2. 確認導入</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="517" />
            <source>可导入直播间</source>
            <translation>可導入直播間</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="519" />
            <source>不会修改旧配置；Cookie、令牌、账号、密码和推送凭据不会导入。</source>
            <translation>不會修改舊設定；Cookie、令牌、帳號、密碼和推送憑證不會匯入。</translation>
        </message>
    </context>
</TS>