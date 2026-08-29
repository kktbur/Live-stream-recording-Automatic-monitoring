<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="pt" sourcelanguage="zh_CN">
    <context>
        <name>RecoBox</name>
        <message>
            <location filename="../network.py" line="16" />
            <source>代理地址必须是主机:端口或 HTTP/HTTPS 地址</source>
            <translation>O proxy deve ser anfitrião:porta ou um URL HTTP/HTTPS</translation>
        </message>
        <message>
            <location filename="../network.py" line="18" />
            <source>代理地址不能包含账号密码</source>
            <translation>O proxy não pode conter utilizador ou palavra-passe</translation>
        </message>
        <message>
            <location filename="../network.py" line="20" />
            <source>代理地址不能包含路径、查询参数或片段</source>
            <translation>O proxy não pode conter caminho, consulta ou fragmento</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="200" />
            <source>仍有直播间正在录制或转换，请先全部暂停并等待收尾完成</source>
            <translation>Uma sala ainda está a gravar ou converter. Pause todas e aguarde a conclusão</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="274" />
            <source>找不到直播间</source>
            <translation>Sala não encontrada</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="277" />
            <source>直播间地址不能为空</source>
            <translation>O URL da sala não pode estar vazio</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="280" />
            <source>该直播间地址已经存在</source>
            <translation>Este URL já existe</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="283" />
            <source>保存目录不能为空</source>
            <translation>A pasta de destino não pode estar vazia</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="291" />
            <source>检测间隔必须是正整数</source>
            <translation>O intervalo deve ser um inteiro positivo</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="293" />
            <source>检测间隔不能低于 30 秒</source>
            <translation>O intervalo não pode ser inferior a 30 segundos</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="299" />
            <location filename="../room_model.py" line="301" />
            <location filename="../view_models.py" line="173" />
            <location filename="../ffmpeg.py" line="28" />
            <source>分段分钟数必须是正整数</source>
            <translation>Os minutos por segmento devem ser um inteiro positivo</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="305" />
            <source>不支持该输出格式</source>
            <translation>Formato de saída não suportado</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="163" />
            <source>默认录制目录不能为空</source>
            <translation>A pasta predefinida não pode estar vazia</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="169" />
            <source>轮询秒数和分段分钟数必须是正整数</source>
            <translation>Segundos de consulta e minutos de segmento devem ser positivos</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="171" />
            <source>轮询间隔不能低于 30 秒</source>
            <translation>A consulta não pode ser inferior a 30 segundos</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="175" />
            <source>磁盘保护阈值必须是 1 至 1024 GB</source>
            <translation>O limite de proteção deve ser de 1 a 1024 GB</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="200" />
            <source>设置保存后校验失败，请重试</source>
            <translation>Falha ao verificar as definições guardadas. Tente novamente</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="236" />
            <source>选择文件夹</source>
            <translation>Selecionar pasta</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="304" />
            <source>预检失败：{error}</source>
            <translation>Falha na pré-verificação: {error}</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="320" />
            <source>导入失败：{error}</source>
            <translation>Falha na importação: {error}</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="81" />
            <source>找不到已锁定的解析源码：{path}</source>
            <translation>Código do resolvedor fixado não encontrado: {path}</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="120" />
            <source>暂不支持该直播间链接</source>
            <translation>Este URL de transmissão ainda não é suportado</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="149" />
            <source>当前锁定版淘宝解析器要求登录会话，Reco Box 不导入账号或 Cookie，因此暂不尝试绕过；后续需要实现匿名公开接口后才能启用。</source>
            <translation>O resolvedor Taobao fixado exige sessão iniciada. O Reco Box não importa contas ou cookies nem contorna a restrição; é necessária uma interface pública anónima.</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="196" />
            <source>该 TwitCasting 直播间要求登录，匿名模式不可用</source>
            <translation>Esta sala TwitCasting exige início de sessão; o modo anónimo está indisponível</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="203" />
            <source>该 TwitCasting 页面无法匿名读取，可能需要登录或已受访问限制</source>
            <translation>Esta página TwitCasting não pode ser lida anonimamente; pode exigir sessão ou estar restrita</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="226" />
            <source>TwitCasting 未返回可录制的公开播放地址</source>
            <translation>O TwitCasting não devolveu URL público gravável</translation>
        </message>
        <message>
            <location filename="../recording.py" line="206" />
            <source>未找到 FFmpeg；开发版需要设置 RECO_BOX_FFMPEG</source>
            <translation>FFmpeg não encontrado; a versão de desenvolvimento deve definir RECO_BOX_FFMPEG</translation>
        </message>
        <message>
            <location filename="../recording.py" line="236" />
            <source>磁盘剩余空间低于 {minimum_free_gb:g} GB，已阻止开始录制</source>
            <translation>Espaço livre inferior a {minimum_free_gb:g} GB; gravação bloqueada</translation>
        </message>
        <message>
            <location filename="../recording.py" line="330" />
            <source>未找到可用直播线路</source>
            <translation>Não foi encontrada rota utilizável</translation>
        </message>
        <message>
            <location filename="../recording.py" line="487" />
            <source>未找到 ffprobe</source>
            <translation>ffprobe não encontrado</translation>
        </message>
        <message>
            <location filename="../recording.py" line="492" />
            <location filename="../media_probe.py" line="95" />
            <source>录制目录中没有媒体文件</source>
            <translation>Não há ficheiros multimédia na pasta de gravação</translation>
        </message>
        <message>
            <location filename="../preview.py" line="16" />
            <location filename="../preview.py" line="36" />
            <location filename="../preview.py" line="41" />
            <source>直播预览</source>
            <translation>Pré-visualização da transmissão</translation>
        </message>
        <message>
            <location filename="../preview.py" line="37" />
            <source>尚未取得直播流，请先点击“立即检查并录制”</source>
            <translation>Ainda não há fluxo. Clique primeiro em «Verificar e gravar agora»</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="85" />
            <source>ffprobe 验证失败</source>
            <translation>Falha na validação do ffprobe</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="89" />
            <source>ffprobe 返回了无效 JSON</source>
            <translation>O ffprobe devolveu JSON inválido</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="112" />
            <source>文件中没有可识别的音视频流</source>
            <translation>Não foi encontrado fluxo de áudio ou vídeo reconhecível</translation>
        </message>
        <message>
            <location filename="../ffmpeg.py" line="26" />
            <source>必须先设置录制保存目录</source>
            <translation>Defina primeiro a pasta de gravação</translation>
        </message>
        <message>
            <location filename="../output_paths.py" line="46" />
            <location filename="../output_paths.py" line="53" />
            <source>输出格式必须是简单扩展名</source>
            <translation>O formato de saída deve ser uma extensão simples</translation>
        </message>
    </context>
    <context>
        <name>Main</name>
        <message>
            <location filename="../ui/Main.qml" line="35" />
            <source>全部状态</source>
            <translation>Todos os status</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="36" />
            <location filename="../ui/Main.qml" line="240" />
            <location filename="../ui/Main.qml" line="439" />
            <source>录制中</source>
            <translation>Gravação</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="37" />
            <location filename="../ui/Main.qml" line="240" />
            <source>监控中</source>
            <translation>Monitoramento</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="38" />
            <location filename="../ui/Main.qml" line="240" />
            <source>未开始</source>
            <translation>Não iniciado</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="41" />
            <source>默认排序</source>
            <translation>Classificação padrão</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="42" />
            <source>名称正序</source>
            <translation>Sequência de nomes</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="43" />
            <source>名称倒序</source>
            <translation>Nome na ordem inversa</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="46" />
            <source>原画</source>
            <translation>Pintura original</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="47" />
            <source>蓝光</source>
            <translation>Blu-ray</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="48" />
            <source>超清</source>
            <translation>Ultra HD</translation>
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
            <translation>Suave</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="54" />
            <source>线路1</source>
            <translation>Linha 1</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="55" />
            <source>线路2</source>
            <translation>Linha 2</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="56" />
            <source>线路3</source>
            <translation>Linha 3</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="57" />
            <source>线路4</source>
            <translation>Linha 4</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="58" />
            <source>线路5</source>
            <translation>Linha 5</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="162" />
            <location filename="../ui/Main.qml" line="279" />
            <location filename="../ui/Main.qml" line="286" />
            <source>添加直播间</source>
            <translation>Adicionar sala de transmissão ao vivo</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="165" />
            <source>一键全部开始录屏 / 监控</source>
            <translation>Comece a gravar/monitorar tudo com um clique</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="166" />
            <source>已启用全部直播间并立即检查</source>
            <translation>Todas as salas de transmissão ao vivo foram habilitadas e verificadas agora</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="169" />
            <source>一键全部暂停录屏 / 监控</source>
            <translation>Pause toda gravação/monitoramento de tela com um clique</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="170" />
            <source>已请求全部暂停；正在录制的文件会先安全收尾</source>
            <translation>Todas as pausas foram solicitadas; os arquivos que estão sendo gravados serão finalizados com segurança primeiro</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="172" />
            <location filename="../ui/Main.qml" line="369" />
            <source>删除全部直播间</source>
            <translation>Excluir todas as salas de transmissão ao vivo</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="174" />
            <source>全局设置、录制历史和运行日志</source>
            <translation>Configurações globais, histórico de gravação e logs de execução</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="180" />
            <source>搜索主播、标题或链接…</source>
            <translation>Busque por âncora, título ou link…</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="188" />
            <source>直播间</source>
            <translation>Sala de transmissão ao vivo</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="240" />
            <source>转 MP4</source>
            <translation>para MP4</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="240" />
            <source>检查中</source>
            <translation>Verificando</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="243" />
            <source>暂无直播间标题</source>
            <translation>Ainda não há título de sala de transmissão ao vivo</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="244" />
            <source>分段：</source>
            <translation>Segmentação:</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="244" />
            <source>每 </source>
            <translation>Cada</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="244" />
            <source> 分钟</source>
            <translation>minutos</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="244" />
            <source>关闭</source>
            <translation>Fechar</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="244" />
            <source> · 完成后转 MP4</source>
            <translation>· Converter para MP4 após a conclusão</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="249" />
            <source>检测间隔 </source>
            <translation>Intervalo de detecção</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="249" />
            <source> 秒</source>
            <translation>segundos</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="253" />
            <source>错误：</source>
            <translation>Erro:</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="258" />
            <source>停止并暂停</source>
            <translation>Parar e pausar</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="258" />
            <source>暂停监控</source>
            <translation>Pausar monitoramento</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="258" />
            <source>开始监控</source>
            <translation>Iniciar monitoramento</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="263" />
            <source>检查并录制</source>
            <translation>Verifique e registre</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="267" />
            <source>预览</source>
            <translation>Visualização</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="268" />
            <source>编辑</source>
            <translation>Editar</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="270" />
            <source>删除</source>
            <translation>Excluir</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="277" />
            <source>还没有直播间</source>
            <translation>Ainda não há sala de transmissão ao vivo</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="277" />
            <source>没有符合当前筛选条件的直播间</source>
            <translation>Não há salas de transmissão ao vivo que atendam às condições atuais de filtro</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="278" />
            <source>添加公开直播间地址后，Reco Box 会自动开始监控</source>
            <translation>Após adicionar o endereço da sala de transmissão pública ao vivo, o Reco Box iniciará automaticamente o monitoramento</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="278" />
            <source>调整状态筛选或搜索关键词后重试</source>
            <translation>Ajuste o filtro de status ou pesquise por palavras-chave e tente novamente</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="289" />
            <source>直播间添加成功</source>
            <translation>Sala de transmissão ao vivo adicionada com sucesso</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="292" />
            <location filename="../ui/Main.qml" line="321" />
            <source>直播间地址</source>
            <translation>Endereço da sala de transmissão ao vivo</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="293" />
            <source>粘贴公开直播间链接</source>
            <translation>Cole o link da sala pública de transmissão ao vivo</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="294" />
            <source>主播名字（可稍后自动识别）</source>
            <translation>Nome da âncora (pode ser reconhecido automaticamente posteriormente)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="295" />
            <source>待识别主播</source>
            <translation>Âncora a ser identificada</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="296" />
            <location filename="../ui/Main.qml" line="334" />
            <source>保存目录</source>
            <translation>Salvar diretório</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="297" />
            <location filename="../ui/Main.qml" line="335" />
            <location filename="../ui/Main.qml" line="409" />
            <source>选择目录</source>
            <translation>Selecionar diretório</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="298" />
            <source>格式、画质、检测间隔和分段使用已保存的全局默认设置。</source>
            <translation>Formato, qualidade, intervalo de detecção e segmentação usam configurações padrão globais salvas.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="305" />
            <source>编辑直播间</source>
            <translation>Editar sala de transmissão ao vivo</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="320" />
            <source>基础编辑</source>
            <translation>Edição básica</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="323" />
            <source>主播名字</source>
            <translation>Nome da âncora</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="325" />
            <source>直播间标题</source>
            <translation>Título da sala de transmissão ao vivo</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="326" />
            <source>可以留空，开播后自动更新</source>
            <translation>pode ser deixado em branco e será atualizado automaticamente após a transmissão.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="328" />
            <source>录制设置</source>
            <translation>Configurações de gravação</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="331" />
            <source>文件名（不分段时使用）</source>
            <translation>Nome do arquivo (usado quando não segmentado)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="331" />
            <source>留空则使用 1</source>
            <translation>Deixe em branco para usar 1</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="332" />
            <location filename="../ui/Main.qml" line="414" />
            <source>检测间隔（秒）</source>
            <translation>Intervalo de detecção (segundos)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="336" />
            <source>代理地址（可选）</source>
            <translation>Endereço proxy (opcional)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="337" />
            <source>例如 127.0.0.1:7890；留空表示直连</source>
            <translation>Por exemplo, 127.0.0.1:7890; deixe em branco para indicar conexão direta</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="340" />
            <source>录制清晰度</source>
            <translation>Nitidez de gravação</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="341" />
            <source>录制路线</source>
            <translation>Registrando rota</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="345" />
            <source>输出格式</source>
            <translation>Formato de saída</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="346" />
            <source>分段时长（分钟）</source>
            <translation>Duração do segmento (minutos)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="346" />
            <source>启用</source>
            <translation>Ativar</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="348" />
            <source>分段文件固定按 1、2、3… 排列，最后一段按实际剩余时长保存。</source>
            <translation>Arquivos segmentados são organizados fixamente em 1, 2, 3..., e o último segmento é salvo de acordo com a duração restante real.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="349" />
            <source>录制完成后转为 MP4（成功后删除 TS）</source>
            <translation>Converter para MP4 após a conclusão da gravação (excluir TS após sucesso)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="350" />
            <source>纯音频模式</source>
            <translation>Modo somente áudio</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="351" />
            <source>录制弹幕（仅在平台适配完成后生效）</source>
            <translation>Record barragens (só terão efeito após a conclusão da adaptação da plataforma)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="358" />
            <location filename="../ui/Main.qml" line="377" />
            <source>取消</source>
            <translation>Cancelar</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="360" />
            <source>保存</source>
            <translation>Salvar</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="361" />
            <source>直播间设置已保存</source>
            <translation>As configurações da sala de transmissão ao vivo foram salvas</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="375" />
            <source>确定从 Reco Box 中删除全部直播间吗？
录制文件和历史记录不会删除。</source>
            <translation>Tem certeza de que deseja excluir todas as salas de transmissão ao vivo do Reco Box?
Os arquivos de gravação e o histórico não serão excluídos.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="377" />
            <source>确认全部删除</source>
            <translation>Confirme a exclusão de todos</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="377" />
            <source>已删除全部直播间</source>
            <translation>Todas as salas de transmissão ao vivo foram excluídas</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="383" />
            <location filename="../ui/Main.qml" line="388" />
            <source>全局设置</source>
            <translation>Configurações globais</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="388" />
            <source>录制历史</source>
            <translation>Histórico de gravação</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="388" />
            <source>运行日志</source>
            <translation>Registro de execução</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="395" />
            <source>新直播间默认设置</source>
            <translation>Configurações padrão para nova sala de transmissão ao vivo</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="395" />
            <source>导入旧配置</source>
            <translation>Importar configuração antiga</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="396" />
            <source>界面语言</source>
            <translation>Linguagem de interface</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="403" />
            <source>界面语言已切换</source>
            <translation>O idioma da interface foi alterado</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="407" />
            <source>只影响以后新增或导入的直播间；已有直播间在卡片中单独编辑。</source>
            <translation>afeta apenas salas de transmissão ao vivo que serão adicionadas ou importadas no futuro; as salas de transmissão ao vivo existentes podem ser editadas separadamente no cartão.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="408" />
            <source>默认录制目录</source>
            <translation>Diretório de gravação padrão</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="412" />
            <source>默认格式</source>
            <translation>Formato padrão</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="413" />
            <source>默认画质</source>
            <translation>Qualidade padrão</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="415" />
            <source>磁盘保护（GB）</source>
            <translation>Proteção de disco (GB)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="417" />
            <source>默认代理地址（可选）</source>
            <translation>Endereço proxy padrão (opcional)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="418" />
            <source>新直播间继承；留空表示直连</source>
            <translation>Nova sala de transmissão ao vivo herdada; deixe em branco para indicar conexão direta</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="419" />
            <source>新直播间默认启用分段</source>
            <translation>Novas salas de transmissão ao vivo permitem segmentação por padrão</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="419" />
            <location filename="../ui/Main.qml" line="420" />
            <source>设置已更改，请点击保存设置</source>
            <translation>As configurações foram alteradas, clique para salvar as configurações</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="420" />
            <source>每段</source>
            <translation>Cada parágrafo</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="420" />
            <source>分钟，最后一段按实际时长保存</source>
            <translation>minutos, o último segmento é salvo de acordo com a duração real</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="423" />
            <source>启动后自动监控 · 关闭窗口最小化到托盘 · 不随 Windows 开机启动</source>
            <translation>Monitorar automaticamente após a inicialização · Fechar a janela e minimizá-la na bandeja · Não iniciar com a inicialização do Windows</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="425" />
            <source>保存设置</source>
            <translation>Salvar configurações</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="425" />
            <source>已保存并确认：以后新增直播间默认每 </source>
            <translation>Salvo e confirmado: o padrão para cada nova sala de transmissão ao vivo no futuro</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="425" />
            <source> 分钟分段</source>
            <translation>segmentos de minutos</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="425" />
            <source>已保存并确认：以后新增直播间默认不分段</source>
            <translation>Salvo e confirmado: Novas salas de transmissão ao vivo não serão segmentadas por padrão no futuro.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="427" />
            <source>已保存并确认</source>
            <translation>Salvo e confirmado</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="427" />
            <source>设置已更改</source>
            <translation>Configurações alteradas</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="439" />
            <source>可播放</source>
            <translation>Pode ser reproduzido</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="439" />
            <source>转 MP4 中</source>
            <translation>Converter para MP4</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="439" />
            <source>已完成</source>
            <translation>Concluído</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="439" />
            <source>失败</source>
            <translation>falhou</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="440" />
            <location filename="../ui/Main.qml" line="505" />
            <source>播放</source>
            <translation>Jogar</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="441" />
            <source>目录</source>
            <translation>Diretório</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="446" />
            <source>这里只显示脱敏后的状态和错误，不保存完整临时播放地址。</source>
            <translation>Apenas o status e os erros após a dessensibilização são exibidos aqui, e o endereço de reprodução temporário completo não é salvo.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="471" />
            <source>直播流播放失败</source>
            <translation>Falha na reprodução da transmissão ao vivo</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="475" />
            <source>直播流格式无效或播放器无法解码</source>
            <translation>O formato da transmissão ao vivo é inválido ou o player não consegue decodificá-lo</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="499" />
            <source>正在准备预览……</source>
            <translation>Preparando para visualização...</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="500" />
            <source>正在连接直播流并等待首帧……</source>
            <translation>Conectando-se à transmissão ao vivo e aguardando o primeiro quadro...</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="505" />
            <source>暂停</source>
            <translation>Pausa</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="505" />
            <source>静音</source>
            <translation>Silenciar</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="511" />
            <source>导入 DouyinLiveRecorder 旧配置</source>
            <translation>Importar configuração antiga do DouyinLiveRecorder</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="515" />
            <source>选择旧程序根目录或其中的 config 文件夹。</source>
            <translation>Selecione o diretório raiz do programa antigo ou a pasta de configuração nele.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="516" />
            <source>选择文件夹</source>
            <translation>Selecionar pasta</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="517" />
            <source>1. 预检</source>
            <translation>1. Pré-verificação</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="517" />
            <source>2. 确认导入</source>
            <translation>2. Confirmar importação</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="517" />
            <source>可导入直播间</source>
            <translation>pode ser importado para a sala de transmissão ao vivo</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="519" />
            <source>不会修改旧配置；Cookie、令牌、账号、密码和推送凭据不会导入。</source>
            <translation>Configurações antigas não serão modificadas; cookies, tokens, contas, senhas e credenciais push não serão importados.</translation>
        </message>
    </context>
</TS>