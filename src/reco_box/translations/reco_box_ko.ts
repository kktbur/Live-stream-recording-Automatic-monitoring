<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="ko" sourcelanguage="zh_CN">
    <context>
        <name>RecoBox</name>
        <message>
            <location filename="../network.py" line="16" />
            <source>代理地址必须是主机:端口或 HTTP/HTTPS 地址</source>
            <translation>프록시는 호스트:포트 또는 HTTP/HTTPS URL이어야 합니다</translation>
        </message>
        <message>
            <location filename="../network.py" line="18" />
            <source>代理地址不能包含账号密码</source>
            <translation>프록시에 사용자 이름이나 비밀번호를 포함할 수 없습니다</translation>
        </message>
        <message>
            <location filename="../network.py" line="20" />
            <source>代理地址不能包含路径、查询参数或片段</source>
            <translation>프록시에 경로, 쿼리 또는 조각을 포함할 수 없습니다</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="200" />
            <source>仍有直播间正在录制或转换，请先全部暂停并等待收尾完成</source>
            <translation>녹화 또는 변환 중인 방이 있습니다. 모두 일시 중지하고 마무리를 기다리세요</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="274" />
            <source>找不到直播间</source>
            <translation>방을 찾을 수 없습니다</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="277" />
            <source>直播间地址不能为空</source>
            <translation>방 URL은 비워 둘 수 없습니다</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="280" />
            <source>该直播间地址已经存在</source>
            <translation>이 방 URL은 이미 존재합니다</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="283" />
            <source>保存目录不能为空</source>
            <translation>저장 폴더는 비워 둘 수 없습니다</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="291" />
            <source>检测间隔必须是正整数</source>
            <translation>확인 간격은 양의 정수여야 합니다</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="293" />
            <source>检测间隔不能低于 30 秒</source>
            <translation>확인 간격은 30초보다 짧을 수 없습니다</translation>
        </message>
        <message>
            <location filename="../ffmpeg.py" line="28" />
            <location filename="../room_model.py" line="299" />
            <location filename="../room_model.py" line="301" />
            <location filename="../view_models.py" line="200" />
            <source>分段分钟数必须是正整数</source>
            <translation>분할 시간은 양의 정수여야 합니다</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="305" />
            <source>不支持该输出格式</source>
            <translation>지원하지 않는 출력 형식입니다</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="187" />
            <source>默认录制目录不能为空</source>
            <translation>기본 녹화 폴더는 비워 둘 수 없습니다</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="198" />
            <source>轮询间隔不能低于 30 秒</source>
            <translation>폴링 간격은 30초보다 짧을 수 없습니다</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="202" />
            <source>磁盘保护阈值必须是 1 至 1024 GB</source>
            <translation>디스크 보호 임계값은 1~1024GB여야 합니다</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="243" />
            <source>设置保存后校验失败，请重试</source>
            <translation>저장된 설정 검증에 실패했습니다. 다시 시도하세요</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="288" />
            <source>选择文件夹</source>
            <translation>폴더 선택</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="356" />
            <source>预检失败：{error}</source>
            <translation>사전 검사 실패: {error}</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="372" />
            <source>导入失败：{error}</source>
            <translation>가져오기 실패: {error}</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="94" />
            <source>找不到已锁定的解析源码：{path}</source>
            <translation>고정된 리졸버 소스를 찾을 수 없음: {path}</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="133" />
            <source>暂不支持该直播间链接</source>
            <translation>이 라이브 URL은 아직 지원되지 않습니다</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="165" />
            <source>当前锁定版淘宝解析器要求登录会话，Reco Box 不导入账号或 Cookie，因此暂不尝试绕过；后续需要实现匿名公开接口后才能启用。</source>
            <translation>고정된 Taobao 리졸버는 로그인 세션을 요구합니다. Reco Box는 계정이나 Cookie를 가져오거나 제한을 우회하지 않으며 공개 익명 인터페이스 구현 후 활성화할 수 있습니다.</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="212" />
            <source>该 TwitCasting 直播间要求登录，匿名模式不可用</source>
            <translation>이 TwitCasting 방은 로그인이 필요하여 익명 모드를 사용할 수 없습니다</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="219" />
            <source>该 TwitCasting 页面无法匿名读取，可能需要登录或已受访问限制</source>
            <translation>이 TwitCasting 페이지는 익명으로 읽을 수 없습니다. 로그인 또는 접근 제한이 있을 수 있습니다</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="243" />
            <source>TwitCasting 未返回可录制的公开播放地址</source>
            <translation>TwitCasting에서 녹화 가능한 공개 URL을 반환하지 않았습니다</translation>
        </message>
        <message>
            <location filename="../recording.py" line="206" />
            <source>未找到 FFmpeg；开发版需要设置 RECO_BOX_FFMPEG</source>
            <translation>FFmpeg를 찾을 수 없습니다. 개발 빌드에서는 RECO_BOX_FFMPEG를 설정하세요</translation>
        </message>
        <message>
            <location filename="../recording.py" line="236" />
            <source>磁盘剩余空间低于 {minimum_free_gb:g} GB，已阻止开始录制</source>
            <translation>남은 공간이 {minimum_free_gb:g}GB 미만이어서 녹화를 시작하지 않았습니다</translation>
        </message>
        <message>
            <location filename="../recording.py" line="330" />
            <source>未找到可用直播线路</source>
            <translation>사용 가능한 라이브 경로를 찾을 수 없습니다</translation>
        </message>
        <message>
            <location filename="../recording.py" line="487" />
            <source>未找到 ffprobe</source>
            <translation>ffprobe를 찾을 수 없습니다</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="95" />
            <location filename="../recording.py" line="492" />
            <source>录制目录中没有媒体文件</source>
            <translation>녹화 폴더에 미디어 파일이 없습니다</translation>
        </message>
        <message>
            <location filename="../preview.py" line="16" />
            <location filename="../preview.py" line="36" />
            <location filename="../preview.py" line="41" />
            <source>直播预览</source>
            <translation>라이브 미리보기</translation>
        </message>
        <message>
            <location filename="../preview.py" line="37" />
            <source>尚未取得直播流，请先点击“立即检查并录制”</source>
            <translation>아직 스트림을 받지 못했습니다. 먼저 ‘지금 확인 및 녹화’를 누르세요</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="85" />
            <source>ffprobe 验证失败</source>
            <translation>ffprobe 검증 실패</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="89" />
            <source>ffprobe 返回了无效 JSON</source>
            <translation>ffprobe가 잘못된 JSON을 반환했습니다</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="112" />
            <source>文件中没有可识别的音视频流</source>
            <translation>인식 가능한 오디오 또는 비디오 스트림이 없습니다</translation>
        </message>
        <message>
            <location filename="../ffmpeg.py" line="26" />
            <source>必须先设置录制保存目录</source>
            <translation>먼저 녹화 저장 폴더를 설정하세요</translation>
        </message>
        <message>
            <location filename="../output_paths.py" line="46" />
            <location filename="../output_paths.py" line="53" />
            <source>输出格式必须是简单扩展名</source>
            <translation>출력 형식은 단순 확장자여야 합니다</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="418" />
            <source>Resolver 调度限制</source>
            <translation>Resolver 스케줄링 제한</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="421" />
            <source>最大并发</source>
            <translation>최대 동시성</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="422" />
            <source>单平台并发</source>
            <translation>플랫폼별 동시성</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="423" />
            <source>平台冷却（秒）</source>
            <translation>플랫폼 쿨다운(초)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="425" />
            <source>用于分散解析请求；修改后立即影响新的监控请求。</source>
            <translation>Resolver 요청을 분산하는 데 사용되며, 변경 사항은 새 모니터링 요청에 즉시 적용됩니다.</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="196" />
            <source>轮询、分段和解析限制参数必须是整数</source>
            <translation>폴링, 세그먼트 및 Resolver 제한 매개변수는 정수여야 합니다</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="204" />
            <source>Resolver 最大并发必须是 1 至 32</source>
            <translation>Resolver 최대 동시성은 1에서 32 사이여야 합니다</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="206" />
            <source>单平台并发必须是 1 至 16</source>
            <translation>플랫폼별 동시성은 1에서 16 사이여야 합니다</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="208" />
            <source>平台冷却必须是 0 至 3600 秒</source>
            <translation>플랫폼 쿨다운은 0에서 3600초 사이여야 합니다</translation>
        </message>
    </context>
    <context>
        <name>Main</name>
        <message>
            <location filename="../ui/Main.qml" line="35" />
            <source>全部状态</source>
            <translation>모든 상태</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="36" />
            <location filename="../ui/Main.qml" line="241" />
            <location filename="../ui/Main.qml" line="448" />
            <source>录制中</source>
            <translation>녹음 중</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="37" />
            <location filename="../ui/Main.qml" line="241" />
            <source>监控中</source>
            <translation>모니터링</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="38" />
            <location filename="../ui/Main.qml" line="241" />
            <source>未开始</source>
            <translation>시작되지 않음</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="41" />
            <source>默认排序</source>
            <translation>기본 정렬</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="42" />
            <source>名称正序</source>
            <translation>이름 순서</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="43" />
            <source>名称倒序</source>
            <translation>이름 역순</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="46" />
            <source>原画</source>
            <translation>원화</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="47" />
            <source>蓝光</source>
            <translation>블루레이</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="48" />
            <source>超清</source>
            <translation>울트라 HD</translation>
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
            <translation>부드러움</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="54" />
            <source>线路1</source>
            <translation>라인 1</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="55" />
            <source>线路2</source>
            <translation>2호선</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="56" />
            <source>线路3</source>
            <translation>3호선</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="57" />
            <source>线路4</source>
            <translation>4호선</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="58" />
            <source>线路5</source>
            <translation>5호선</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="163" />
            <location filename="../ui/Main.qml" line="280" />
            <location filename="../ui/Main.qml" line="287" />
            <source>添加直播间</source>
            <translation>실시간 방송방 추가</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="166" />
            <source>一键全部开始录屏 / 监控</source>
            <translation>클릭 한 번으로 녹화/모니터링을 모두 시작하세요</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="167" />
            <source>已启用全部直播间并立即检查</source>
            <translation>모든 실시간 방송방이 활성화되어 확인되었습니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="170" />
            <source>一键全部暂停录屏 / 监控</source>
            <translation>한 번의 클릭으로 모든 화면 녹화/모니터링을 일시 중지합니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="171" />
            <source>已请求全部暂停；正在录制的文件会先安全收尾</source>
            <translation>모든 일시중지가 요청되었습니다. 녹화 중인 파일이 먼저 안전하게 종료됩니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="173" />
            <location filename="../ui/Main.qml" line="370" />
            <source>删除全部直播间</source>
            <translation>모든 실시간 방송방 삭제</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="175" />
            <source>全局设置、录制历史和运行日志</source>
            <translation>전체 설정, 기록 내역 및 실행 로그</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="181" />
            <source>搜索主播、标题或链接…</source>
            <translation>앵커, 제목, 링크 검색…</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="189" />
            <source>直播间</source>
            <translation>생방송실</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="241" />
            <source>转 MP4</source>
            <translation>MP4로</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="241" />
            <source>检查中</source>
            <translation>확인 중</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="244" />
            <source>暂无直播间标题</source>
            <translation>아직 생방송 방 제목이 없습니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source>分段：</source>
            <translation>분할:</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source>每 </source>
            <translation>매번</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source> 分钟</source>
            <translation>분</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source>关闭</source>
            <translation>닫기</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source> · 完成后转 MP4</source>
            <translation>· 완료 후 MP4로 변환</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="250" />
            <source>检测间隔 </source>
            <translation>감지 간격</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="250" />
            <source> 秒</source>
            <translation>초</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="254" />
            <source>错误：</source>
            <translation>오류:</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="259" />
            <source>停止并暂停</source>
            <translation>중지 및 일시 중지</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="259" />
            <source>暂停监控</source>
            <translation>모니터링 일시중지</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="259" />
            <source>开始监控</source>
            <translation>모니터링 시작</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="264" />
            <source>检查并录制</source>
            <translation>확인 및 기록</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="268" />
            <source>预览</source>
            <translation>미리보기</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="269" />
            <source>编辑</source>
            <translation>편집</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="271" />
            <source>删除</source>
            <translation>삭제</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="278" />
            <source>还没有直播间</source>
            <translation>아직 생방송 방이 없습니다</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="278" />
            <source>没有符合当前筛选条件的直播间</source>
            <translation>현재 필터 조건을 만족하는 생방송 방이 없습니다</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="279" />
            <source>添加公开直播间地址后，Reco Box 会自动开始监控</source>
            <translation>공개 생방송 방 주소를 추가하면 레코박스가 자동으로 모니터링을 시작합니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="279" />
            <source>调整状态筛选或搜索关键词后重试</source>
            <translation>상태 필터를 조정하거나 키워드를 검색한 후 다시 시도하세요.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="290" />
            <source>直播间添加成功</source>
            <translation>생방송 방이 추가되었습니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="293" />
            <location filename="../ui/Main.qml" line="322" />
            <source>直播间地址</source>
            <translation>생방송 방 주소</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="294" />
            <source>粘贴公开直播间链接</source>
            <translation>공개 생방송 방 링크 붙여넣기</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="295" />
            <source>主播名字（可稍后自动识别）</source>
            <translation>앵커 이름(추후 자동 인식 가능)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="296" />
            <source>待识别主播</source>
            <translation>식별할 앵커</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="297" />
            <location filename="../ui/Main.qml" line="335" />
            <source>保存目录</source>
            <translation>저장 디렉토리</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="298" />
            <location filename="../ui/Main.qml" line="336" />
            <location filename="../ui/Main.qml" line="410" />
            <source>选择目录</source>
            <translation>디렉터리 선택</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="299" />
            <source>格式、画质、检测间隔和分段使用已保存的全局默认设置。</source>
            <translation>형식, 품질, 감지 간격 및 분할은 저장된 전역 기본 설정을 사용합니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="306" />
            <source>编辑直播间</source>
            <translation>실시간 방송방 편집</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="321" />
            <source>基础编辑</source>
            <translation>기본 편집</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="324" />
            <source>主播名字</source>
            <translation>앵커 이름</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="326" />
            <source>直播间标题</source>
            <translation>생방송 방 제목</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="327" />
            <source>可以留空，开播后自动更新</source>
            <translation>은 비워둘 수 있으며 방송 후 자동으로 업데이트됩니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="329" />
            <source>录制设置</source>
            <translation>녹화 설정</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="332" />
            <source>文件名（不分段时使用）</source>
            <translation>파일 이름(분할되지 않은 경우 사용)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="332" />
            <source>留空则使用 1</source>
            <translation>1을 사용하려면 비워 두세요.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="333" />
            <location filename="../ui/Main.qml" line="415" />
            <source>检测间隔（秒）</source>
            <translation>감지 간격(초)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="337" />
            <source>代理地址（可选）</source>
            <translation>프록시 주소(선택 사항)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="338" />
            <source>例如 127.0.0.1:7890；留空表示直连</source>
            <translation>예: 127.0.0.1:7890; 직접 연결을 나타내려면 비워 두세요.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="341" />
            <source>录制清晰度</source>
            <translation>녹음 선명도</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="342" />
            <source>录制路线</source>
            <translation>녹음 경로</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="346" />
            <source>输出格式</source>
            <translation>출력 형식</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="347" />
            <source>分段时长（分钟）</source>
            <translation>세그먼트 기간(분)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="347" />
            <source>启用</source>
            <translation>활성화</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="349" />
            <source>分段文件固定按 1、2、3… 排列，最后一段按实际剩余时长保存。</source>
            <translation>분할된 파일은 1, 2, 3...으로 고정되어 있으며 마지막 부분은 실제 남은 시간에 따라 저장됩니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="350" />
            <source>录制完成后转为 MP4（成功后删除 TS）</source>
            <translation>녹화 완료 후 MP4로 변환 (성공 후 TS 삭제)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="351" />
            <source>纯音频模式</source>
            <translation>오디오 전용 모드</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="352" />
            <source>录制弹幕（仅在平台适配完成后生效）</source>
            <translation>기록 사격(플랫폼 적응이 완료된 후에만 적용됩니다)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="359" />
            <location filename="../ui/Main.qml" line="378" />
            <source>取消</source>
            <translation>취소</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="361" />
            <source>保存</source>
            <translation>저장</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="362" />
            <source>直播间设置已保存</source>
            <translation>생방송 방 설정이 저장되었습니다</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="376" />
            <source>确定从 Reco Box 中删除全部直播间吗？
录制文件和历史记录不会删除。</source>
            <translation>Reco Box에서 모든 라이브 방송방을 삭제하시겠습니까?
녹화 파일 및 기록은 삭제되지 않습니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="378" />
            <source>确认全部删除</source>
            <translation>모두 삭제 확인</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="378" />
            <source>已删除全部直播间</source>
            <translation>모든 생방송 방이 삭제되었습니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="384" />
            <location filename="../ui/Main.qml" line="389" />
            <source>全局设置</source>
            <translation>전역 설정</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="389" />
            <source>录制历史</source>
            <translation>녹화 내역</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="389" />
            <source>运行日志</source>
            <translation>실행 로그</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="396" />
            <source>新直播间默认设置</source>
            <translation>새 생방송 방의 기본 설정</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="396" />
            <source>导入旧配置</source>
            <translation>이전 구성 가져오기</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="397" />
            <source>界面语言</source>
            <translation>인터페이스 언어</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="404" />
            <source>界面语言已切换</source>
            <translation>인터페이스 언어가 변경되었습니다</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="408" />
            <source>只影响以后新增或导入的直播间；已有直播间在卡片中单独编辑。</source>
            <translation>는 향후 추가되거나 가져올 라이브 방송실에만 영향을 미칩니다. 기존 생방송 방은 카드에서 별도로 편집할 수 있습니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="409" />
            <source>默认录制目录</source>
            <translation>기본 녹화 디렉터리</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="413" />
            <source>默认格式</source>
            <translation>기본 형식</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="414" />
            <source>默认画质</source>
            <translation>기본 품질</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="416" />
            <source>磁盘保护（GB）</source>
            <translation>디스크 보호(GB)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="426" />
            <source>默认代理地址（可选）</source>
            <translation>기본 프록시 주소(선택 사항)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="427" />
            <source>新直播间继承；留空表示直连</source>
            <translation>새 생방송 방이 상속됩니다. 직접 연결을 나타내려면 비워 두세요.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="428" />
            <source>新直播间默认启用分段</source>
            <translation>새로운 라이브 방송실에서는 기본적으로 분할이 가능합니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="428" />
            <location filename="../ui/Main.qml" line="429" />
            <source>设置已更改，请点击保存设置</source>
            <translation>설정이 변경되었습니다. 설정을 저장하려면 클릭하세요.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="429" />
            <source>每段</source>
            <translation>각 문단</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="429" />
            <source>分钟，最后一段按实际时长保存</source>
            <translation>분, 실제 지속 시간에 따라 마지막 세그먼트가 저장됩니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="432" />
            <source>启动后自动监控 · 关闭窗口最小化到托盘 · 不随 Windows 开机启动</source>
            <translation>시작 후 자동으로 모니터링 · 창을 닫고 트레이로 최소화 · Windows 시작 시 시작하지 않음</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source>保存设置</source>
            <translation>설정 저장</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source>已保存并确认：以后新增直播间默认每 </source>
            <translation>저장 및 확인: 향후 각각의 새로운 생방송 방에 대한 기본값</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source> 分钟分段</source>
            <translation>분 세그먼트</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source>已保存并确认：以后新增直播间默认不分段</source>
            <translation>저장 및 확인 : 앞으로 새로운 생방송 방은 기본적으로 분할되지 않습니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="436" />
            <source>已保存并确认</source>
            <translation>저장 및 확인됨</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="436" />
            <source>设置已更改</source>
            <translation>설정이 변경되었습니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>可播放</source>
            <translation>재생 가능</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>转 MP4 中</source>
            <translation>MP4로 변환</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>已完成</source>
            <translation>완료됨</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>失败</source>
            <translation>실패함</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="449" />
            <location filename="../ui/Main.qml" line="514" />
            <source>播放</source>
            <translation>재생</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="450" />
            <source>目录</source>
            <translation>디렉토리</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="455" />
            <source>这里只显示脱敏后的状态和错误，不保存完整临时播放地址。</source>
            <translation>감도 저하 후의 상태와 오류만 여기에 표시되며 전체 임시 재생 주소는 저장되지 않습니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="480" />
            <source>直播流播放失败</source>
            <translation>라이브 스트림 재생 실패</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="484" />
            <source>直播流格式无效或播放器无法解码</source>
            <translation>라이브 스트림 형식이 잘못되었거나 플레이어에서 디코딩할 수 없습니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="508" />
            <source>正在准备预览……</source>
            <translation>미리보기 준비 중...</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="509" />
            <source>正在连接直播流并等待首帧……</source>
            <translation>라이브 스트림에 연결하고 첫 번째 프레임을 기다리는 중...</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="514" />
            <source>暂停</source>
            <translation>일시중지</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="514" />
            <source>静音</source>
            <translation>음소거</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="520" />
            <source>导入 DouyinLiveRecorder 旧配置</source>
            <translation>DouyinLiveRecorder 이전 구성 가져오기</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="524" />
            <source>选择旧程序根目录或其中的 config 文件夹。</source>
            <translation>이전 프로그램 루트 디렉터리 또는 그 안에 있는 config 폴더를 선택합니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="525" />
            <source>选择文件夹</source>
            <translation>폴더 선택</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="526" />
            <source>1. 预检</source>
            <translation>1. 사전 확인</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="526" />
            <source>2. 确认导入</source>
            <translation>2. 가져오기 확인</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="526" />
            <source>可导入直播间</source>
            <translation>을(를) 생방송 방으로 가져올 수 있습니다.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="528" />
            <source>不会修改旧配置；Cookie、令牌、账号、密码和推送凭据不会导入。</source>
            <translation>이전 구성은 수정되지 않습니다. 쿠키, 토큰, 계정, 비밀번호, 푸시 자격 증명은 가져오지 않습니다.</translation>
        </message>
    </context>
</TS>