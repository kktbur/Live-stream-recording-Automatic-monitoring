import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtMultimedia

ApplicationWindow {
    id: window
    width: 1280; height: 820; minimumWidth: 980; minimumHeight: 650
    visible: true; title: "Reco Box"; color: appBackground
    onClosing: function(close) { close.accepted = false; window.hide() }

    // Semantic design tokens. Keep visual decisions centralized so future UI
    // iterations do not accumulate one-off colors and spacing values.
    property color appBackground: "#F4F5F7"
    property color surface: "#FFFFFF"
    property color surfaceSubtle: "#F7F8FA"
    property color surfaceStrong: "#ECEFF3"
    property color ink: "#16181D"
    property color muted: "#626A76"
    property color disabledText: "#A8AEB7"
    property color lineColor: "#DDE1E6"
    property color primary: "#17191D"
    property color primaryHover: "#2A2D33"
    property color primaryText: "#FFFFFF"
    property color success: "#168A4C"
    property color successSoft: "#E8F6EE"
    property color warning: "#A85D00"
    property color warningSoft: "#FFF3DF"
    property color danger: "#B83232"
    property color dangerSoft: "#FBECEC"
    property color focusColor: "#2563EB"
    property string settingsMessage: ""
    property string operationMessage: ""
    property var statusOptions: [
        { value: "all", text: qsTr("全部状态") },
        { value: "recording", text: qsTr("录制中") },
        { value: "monitoring", text: qsTr("监控中") },
        { value: "not_started", text: qsTr("未开始") }
    ]
    property var sortOptions: [
        { value: "default", text: qsTr("默认排序") },
        { value: "name_asc", text: qsTr("名称正序") },
        { value: "name_desc", text: qsTr("名称倒序") }
    ]
    property var qualityOptions: [
        { value: "原画", text: qsTr("原画") },
        { value: "蓝光", text: qsTr("蓝光") },
        { value: "超清", text: qsTr("超清") },
        { value: "高清", text: qsTr("高清") },
        { value: "标清", text: qsTr("标清") },
        { value: "流畅", text: qsTr("流畅") }
    ]
    property var lineOptions: [
        { value: "线路1", text: qsTr("线路1") },
        { value: "线路2", text: qsTr("线路2") },
        { value: "线路3", text: qsTr("线路3") },
        { value: "线路4", text: qsTr("线路4") },
        { value: "线路5", text: qsTr("线路5") }
    ]

    palette.window: appBackground
    palette.windowText: ink
    palette.base: surface
    palette.text: ink
    palette.button: surfaceStrong
    palette.buttonText: ink
    palette.highlight: focusColor
    palette.highlightedText: primaryText
    palette.placeholderText: muted

    function durationText(seconds) {
        const h = Math.floor(seconds / 3600), m = Math.floor((seconds % 3600) / 60), s = seconds % 60
        return String(h).padStart(2, "0") + ":" + String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0")
    }
    function bytesText(bytes) {
        bytes = Math.max(0, Number(bytes) || 0)
        if (bytes < 1024) return bytes + " B"
        if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB"
        if (bytes < 1073741824) return (bytes / 1048576).toFixed(1) + " MB"
        return (bytes / 1073741824).toFixed(2) + " GB"
    }
    function optionIndex(model, value) {
        for (let index = 0; index < model.length; index++) {
            if (model[index].value === value) return index
        }
        return 0
    }

    component ToolIconButton: Button {
        id: control
        property string hint: ""
        property string tone: "neutral"
        implicitWidth: 44; implicitHeight: 44; font.pixelSize: 18
        hoverEnabled: true; activeFocusOnTab: true
        Accessible.name: hint
        ToolTip.visible: hovered; ToolTip.text: hint; ToolTip.delay: 350
        contentItem: Text {
            text: control.text
            color: !control.enabled ? window.disabledText
                : control.tone === "primary" ? window.primaryText
                : control.tone === "positive" ? window.success
                : control.tone === "danger" ? window.danger : window.ink
            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
            font.pixelSize: control.font.pixelSize; font.bold: true
        }
        background: Rectangle {
            color: !control.enabled ? "transparent"
                : control.tone === "primary" ? (control.down ? "#0D0E10" : control.hovered ? window.primaryHover : window.primary)
                : control.tone === "positive" ? (control.down ? "#D4EDDE" : control.hovered ? "#DEF2E6" : window.successSoft)
                : control.tone === "danger" ? (control.down ? "#F5DADA" : control.hovered ? "#F8E3E3" : window.dangerSoft)
                : control.down ? "#E2E5E9" : control.hovered ? window.surfaceStrong : "transparent"
            radius: 10
            border.width: control.activeFocus ? 2 : (control.tone === "neutral" ? 0 : 1)
            border.color: control.activeFocus ? window.focusColor
                : control.tone === "positive" ? "#CBE8D7"
                : control.tone === "danger" ? "#F1CECE"
                : control.tone === "primary" ? window.primary : "transparent"
        }
    }

    component AppButton: Button {
        id: control
        property string tone: "secondary"
        property bool compact: false
        implicitHeight: compact ? 36 : 40
        implicitWidth: Math.max(compact ? 78 : 96, contentItem.implicitWidth + 28)
        leftPadding: 14; rightPadding: 14
        hoverEnabled: true; activeFocusOnTab: true
        contentItem: Text {
            text: control.text
            color: !control.enabled ? window.disabledText
                : control.tone === "primary" || control.tone === "dangerSolid" ? window.primaryText
                : control.tone === "positive" ? window.success
                : control.tone === "danger" ? window.danger : window.ink
            font.pixelSize: 12; font.weight: Font.DemiBold
            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
        }
        background: Rectangle {
            color: !control.enabled ? window.surfaceStrong
                : control.tone === "primary" ? (control.down ? "#0D0E10" : control.hovered ? window.primaryHover : window.primary)
                : control.tone === "dangerSolid" ? (control.down ? "#8F2525" : control.hovered ? "#A92D2D" : window.danger)
                : control.tone === "positive" ? (control.down ? "#D4EDDE" : control.hovered ? "#DEF2E6" : window.successSoft)
                : control.tone === "danger" ? (control.down ? "#F5DADA" : control.hovered ? "#F8E3E3" : window.dangerSoft)
                : control.down ? "#DEE2E7" : control.hovered ? "#E7EAEE" : window.surfaceStrong
            radius: 9
            border.width: control.activeFocus ? 2 : 1
            border.color: control.activeFocus ? window.focusColor
                : control.tone === "danger" ? "#EDCACA"
                : control.tone === "positive" ? "#C8E6D4"
                : control.tone === "primary" || control.tone === "dangerSolid" ? color : window.lineColor
        }
    }

    header: ToolBar {
        height: 78
        background: Rectangle { color: window.surface; border.color: window.lineColor }
        RowLayout {
            anchors.fill: parent; anchors.leftMargin: 26; anchors.rightMargin: 26; spacing: 8
            Image { source: "../../../assets/reco-box-icon-final.png"; sourceSize.width: 40; sourceSize.height: 40; Layout.preferredWidth: 40; Layout.preferredHeight: 40; fillMode: Image.PreserveAspectFit }
            Label { text: "Reco Box"; color: window.ink; font.pixelSize: 18; font.weight: Font.DemiBold }
            Label { objectName: "applicationVersionLabel"; text: "v" + applicationVersion; color: window.muted; font.pixelSize: 11; Layout.rightMargin: 18 }
            ToolIconButton { text: "+"; hint: qsTr("添加直播间"); tone: "primary"; onClicked: addDialog.open() }
            Rectangle { Layout.preferredWidth: 1; Layout.preferredHeight: 26; color: window.lineColor }
            ToolIconButton {
                text: "▶"; hint: qsTr("一键全部开始录屏 / 监控"); tone: "positive"; enabled: roomModel.count > 0
                onClicked: { roomModel.setAllEnabled(true); monitorCoordinator.checkAllNow(); window.operationMessage = qsTr("已启用全部直播间并立即检查") }
            }
            ToolIconButton {
                text: "■"; hint: qsTr("一键全部暂停录屏 / 监控"); enabled: roomModel.count > 0
                onClicked: { recordingManager.stopAllAndPause(); window.operationMessage = qsTr("已请求全部暂停；正在录制的文件会先安全收尾") }
            }
            ToolIconButton { text: "⌫"; hint: qsTr("删除全部直播间"); tone: "danger"; enabled: roomModel.count > 0; onClicked: deleteAllDialog.open() }
            ToolIconButton {
                text: "⚙"; hint: qsTr("全局设置、录制历史和运行日志")
                onClicked: { historyModel.refresh(); eventLogModel.refresh(); globalDialog.open() }
            }
            Item { Layout.fillWidth: true }
            ComboBox { id: statusFilter; model: window.statusOptions; textRole: "text"; valueRole: "value"; Layout.preferredWidth: 154; Layout.preferredHeight: 42; onActivated: roomProxyModel.setStatusFilter(currentValue); background: Rectangle { color: window.surfaceSubtle; radius: 10; border.width: statusFilter.activeFocus ? 2 : 1; border.color: statusFilter.activeFocus ? window.focusColor : window.lineColor } }
            ComboBox { id: sortFilter; model: window.sortOptions; textRole: "text"; valueRole: "value"; Layout.preferredWidth: 154; Layout.preferredHeight: 42; onActivated: roomProxyModel.setSortMode(currentValue); background: Rectangle { color: window.surfaceSubtle; radius: 10; border.width: sortFilter.activeFocus ? 2 : 1; border.color: sortFilter.activeFocus ? window.focusColor : window.lineColor } }
            TextField { id: searchField; placeholderText: qsTr("搜索主播、标题或链接…"); Layout.preferredWidth: 220; Layout.preferredHeight: 42; leftPadding: 16; rightPadding: 14; onTextChanged: roomProxyModel.setSearchText(text); background: Rectangle { color: window.surfaceSubtle; radius: 10; border.width: searchField.activeFocus ? 2 : 1; border.color: searchField.activeFocus ? window.focusColor : window.lineColor } }
        }
    }

    ColumnLayout {
        anchors.fill: parent; anchors.margins: 24; spacing: 12
        RowLayout {
            Layout.fillWidth: true
            Label { text: qsTr("直播间"); color: window.ink; font.pixelSize: 26; font.weight: Font.DemiBold }
            Rectangle { implicitWidth: roomCountLabel.implicitWidth + 16; implicitHeight: 26; radius: 8; color: window.surfaceStrong; Label { id: roomCountLabel; anchors.centerIn: parent; text: roomProxyModel.count + " / " + roomModel.count; color: window.muted; font.pixelSize: 11; font.weight: Font.DemiBold } }
            Item { Layout.fillWidth: true }
            Label { visible: window.operationMessage.length > 0; text: window.operationMessage; color: window.success; font.pixelSize: 11; font.weight: Font.DemiBold }
        }
        GridView {
            id: roomGrid
            Layout.fillWidth: true; Layout.fillHeight: true; clip: true
            cellWidth: width >= 1140 ? width / 3 : width / 2; cellHeight: 306; model: roomProxyModel
            ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }
            delegate: Item {
                required property string roomId
                required property string streamerName
                required property string platformName
                required property string roomUrl
                required property string roomStatus
                required property bool roomEnabled
                required property string qualityName
                required property string lastError
                required property string roomTitle
                required property string saveRoot
                required property string outputFormat
                required property bool segmentEnabled
                required property int segmentMinutes
                required property bool audioOnly
                required property bool recordDanmaku
                required property int durationSeconds
                // QML int is signed 32-bit and overflows once a recording grows
                // beyond 2 GiB. Keep byte counts as a double/JS number.
                required property double fileBytes
                required property bool convertToMp4
                required property string recordingLine
                required property int checkIntervalSeconds
                required property string fileName
                required property string roomProxy
                width: roomGrid.cellWidth; height: roomGrid.cellHeight
                Rectangle {
                    anchors.fill: parent; anchors.rightMargin: 14; anchors.bottomMargin: 14
                    radius: 16; color: window.surface; border.width: roomStatus === "recording" || roomStatus === "stalled" ? 2 : 1; border.color: roomStatus === "recording" ? window.success : roomStatus === "stalled" ? window.warning : window.lineColor
                    ColumnLayout {
                        anchors.fill: parent; anchors.margins: 16; spacing: 7
                        RowLayout {
                            Layout.fillWidth: true
                            Rectangle { Layout.preferredWidth: 44; Layout.preferredHeight: 44; radius: 12; color: window.surfaceStrong; Label { anchors.centerIn: parent; text: platformName === "unknown" ? "?" : platformName.substring(0, 1).toUpperCase(); color: window.ink; font.pixelSize: 14; font.weight: Font.DemiBold } }
                            ColumnLayout {
                                Layout.fillWidth: true; spacing: 1
                                Label { text: streamerName; color: window.ink; font.pixelSize: 16; font.weight: Font.DemiBold; elide: Text.ElideRight; Layout.fillWidth: true; ToolTip.visible: truncated && hovered; ToolTip.text: text }
                                Label { text: roomUrl; color: window.muted; font.pixelSize: 11; elide: Text.ElideMiddle; Layout.fillWidth: true; ToolTip.visible: truncated && hovered; ToolTip.text: text }
                            }
                            Rectangle {
                                implicitWidth: statusLabel.implicitWidth + 18; implicitHeight: 28; radius: 14
                                color: roomStatus === "recording" ? window.successSoft : roomStatus === "stalled" ? window.warningSoft : roomEnabled ? window.surfaceStrong : window.dangerSoft
                                Label { id: statusLabel; anchors.centerIn: parent; text: roomStatus === "recording" ? qsTr("录制中") : roomStatus === "stalled" ? qsTr("卡顿收尾") : roomStatus === "converting" ? qsTr("转 MP4") : roomStatus === "checking" || roomStatus === "preparing" ? qsTr("检查中") : roomEnabled ? qsTr("监控中") : qsTr("未开始"); color: roomStatus === "recording" ? window.success : roomStatus === "stalled" ? window.warning : roomEnabled ? window.muted : window.danger; font.pixelSize: 11; font.weight: Font.DemiBold }
                            }
                        }
                        Label { text: roomTitle.length > 0 ? roomTitle : qsTr("暂无直播间标题"); color: window.muted; font.pixelSize: 12; elide: Text.ElideRight; Layout.fillWidth: true }
                        Label { text: qsTr("分段：") + (segmentEnabled ? qsTr("每 ") + segmentMinutes + qsTr(" 分钟") : qsTr("关闭")) + (convertToMp4 ? qsTr(" · 完成后转 MP4") : ""); color: window.success; font.pixelSize: 11; font.weight: Font.DemiBold; Layout.fillWidth: true }
                        Rectangle {
                            Layout.fillWidth: true; Layout.preferredHeight: 50; radius: 10; color: window.surfaceSubtle; border.width: 1; border.color: "#ECEEF1"
                            RowLayout {
                                anchors.fill: parent; anchors.margins: 10
                                ColumnLayout { Layout.fillWidth: true; spacing: 1; Label { text: qualityName + " · " + outputFormat.toUpperCase() + " · " + recordingLine; color: window.ink; font.pixelSize: 11; font.weight: Font.DemiBold } Label { text: roomStatus === "recording" || roomStatus === "stalled" ? window.durationText(durationSeconds) : qsTr("检测间隔 ") + checkIntervalSeconds + qsTr(" 秒"); color: window.muted; font.pixelSize: 11; font.family: roomStatus === "recording" || roomStatus === "stalled" ? "Consolas" : "" } }
                                Label { objectName: "roomFileSize"; text: window.bytesText(fileBytes); color: window.muted; font.pixelSize: 10 }
                            }
                        }
                        Label { visible: lastError.length > 0; text: qsTr("错误：") + lastError; color: window.danger; font.pixelSize: 10; elide: Text.ElideRight; Layout.fillWidth: true; ToolTip.visible: truncated && hovered; ToolTip.text: text }
                        Item { Layout.fillHeight: true }
                        RowLayout {
                            Layout.fillWidth: true; spacing: 6
                            AppButton {
                                text: roomStatus === "recording" || roomStatus === "stalled" || roomStatus === "retrying" || roomStatus === "converting" ? qsTr("停止并暂停") : roomEnabled ? qsTr("暂停监控") : qsTr("开始监控")
                                tone: roomStatus === "recording" || roomStatus === "stalled" || roomStatus === "retrying" || roomStatus === "converting" ? "danger" : roomEnabled ? "secondary" : "positive"
                                Layout.fillWidth: true
                                onClicked: { if (roomEnabled) recordingManager.stop_room(roomId); else { roomModel.toggleRoom(roomId); monitorCoordinator.checkNow(roomId) } }
                            }
                            AppButton { text: qsTr("检查并录制"); tone: "primary"; Layout.fillWidth: true; enabled: roomEnabled && roomStatus !== "recording" && roomStatus !== "stalled" && roomStatus !== "converting" && roomStatus !== "preparing"; onClicked: monitorCoordinator.checkNow(roomId) }
                        }
                        RowLayout {
                            Layout.fillWidth: true; spacing: 6
                            AppButton { objectName: "previewButton"; text: qsTr("预览"); compact: true; onClicked: { previewController.play(roomId); previewDialog.open() } }
                            AppButton { text: qsTr("编辑"); compact: true; enabled: roomStatus !== "recording" && roomStatus !== "stalled" && roomStatus !== "converting" && roomStatus !== "preparing"; onClicked: editDialog.openFor(roomId, streamerName, roomTitle, roomUrl, fileName, checkIntervalSeconds, saveRoot, roomProxy, outputFormat, qualityName, recordingLine, segmentEnabled, segmentMinutes, convertToMp4, audioOnly, recordDanmaku) }
                            Item { Layout.fillWidth: true }
                            AppButton { text: qsTr("删除"); tone: "danger"; compact: true; enabled: roomStatus !== "recording" && roomStatus !== "stalled" && roomStatus !== "converting" && roomStatus !== "preparing"; onClicked: roomModel.removeRoom(roomId) }
                        }
                    }
                }
            }
            Column {
                anchors.centerIn: parent; visible: roomProxyModel.count === 0; spacing: 12
                Label { anchors.horizontalCenter: parent.horizontalCenter; text: roomModel.count === 0 ? qsTr("还没有直播间") : qsTr("没有符合当前筛选条件的直播间"); color: window.ink; font.pixelSize: 17; font.weight: Font.DemiBold }
                Label { anchors.horizontalCenter: parent.horizontalCenter; text: roomModel.count === 0 ? qsTr("添加公开直播间地址后，Reco Box 会自动开始监控") : qsTr("调整状态筛选或搜索关键词后重试"); color: window.muted; font.pixelSize: 12 }
                AppButton { anchors.horizontalCenter: parent.horizontalCenter; visible: roomModel.count === 0; text: qsTr("添加直播间"); tone: "primary"; onClicked: addDialog.open() }
            }
        }
    }

    Dialog {
        id: addDialog
        title: qsTr("添加直播间"); modal: true; anchors.centerIn: parent; width: 540
        standardButtons: Dialog.Ok | Dialog.Cancel
        background: Rectangle { color: window.surface; radius: 16; border.width: 1; border.color: window.lineColor }
        onAccepted: { const root = folderField.text.trim().length > 0 ? folderField.text : settingsController.defaultSaveRoot; if (roomModel.addRoom(urlField.text, nameField.text, root)) { urlField.clear(); nameField.clear(); folderField.clear(); window.operationMessage = qsTr("直播间添加成功") } }
        ColumnLayout {
            width: parent.width; spacing: 10
            Label { text: qsTr("直播间地址") }
            TextField { id: urlField; Layout.fillWidth: true; placeholderText: qsTr("粘贴公开直播间链接") }
            Label { text: qsTr("主播名字（可稍后自动识别）") }
            TextField { id: nameField; Layout.fillWidth: true; placeholderText: qsTr("待识别主播") }
            Label { text: qsTr("保存目录") }
            RowLayout { Layout.fillWidth: true; TextField { id: folderField; Layout.fillWidth: true; placeholderText: settingsController.defaultSaveRoot } AppButton { text: qsTr("选择目录"); onClicked: { const value = desktopActions.chooseDirectory(folderField.text); if (value.length > 0) folderField.text = value } } }
            Label { text: qsTr("格式、画质、检测间隔和分段使用已保存的全局默认设置。"); color: window.muted; font.pixelSize: 11 }
        }
    }

    Dialog {
        id: editDialog
        objectName: "editDialog"
        title: qsTr("编辑直播间"); modal: true; anchors.centerIn: parent; width: 680; height: 650
        background: Rectangle { color: window.surface; radius: 16; border.width: 1; border.color: window.lineColor }
        property string roomId: ""
        property string errorText: ""
        function openFor(id, name, title, url, fileName, interval, root, proxy, format, quality, line, segmented, minutes, convert, audio, danmaku) {
            roomId = id; editName.text = name; editTitle.text = title; editUrl.text = url; editFileName.text = fileName.length > 0 ? fileName : name; editInterval.text = String(interval); editRoot.text = root; editProxy.text = proxy
            editFormat.currentIndex = Math.max(0, editFormat.model.indexOf(format)); editQuality.currentIndex = window.optionIndex(window.qualityOptions, quality); editLine.currentIndex = window.optionIndex(window.lineOptions, line === "自动" ? "线路1" : line)
            editSegment.checked = segmented; editMinutes.text = minutes > 0 ? String(minutes) : "5"; editConvert.checked = convert; editAudio.checked = audio; editDanmaku.checked = danmaku; errorText = ""; open()
        }
        ColumnLayout {
            anchors.fill: parent; spacing: 10
            ScrollView {
                Layout.fillWidth: true; Layout.fillHeight: true; clip: true; ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                ColumnLayout {
                    width: editDialog.availableWidth - 18; spacing: 10
                    Label { text: qsTr("基础编辑"); color: window.ink; font.pixelSize: 17; font.bold: true }
                    Label { text: qsTr("直播间地址") }
                    TextField { id: editUrl; Layout.fillWidth: true }
                    Label { text: qsTr("主播名字") }
                    TextField { id: editName; Layout.fillWidth: true }
                    Label { text: qsTr("直播间标题") }
                    TextField { id: editTitle; Layout.fillWidth: true; placeholderText: qsTr("可以留空，开播后自动更新") }
                    Rectangle { Layout.fillWidth: true; Layout.preferredHeight: 1; color: window.lineColor; Layout.topMargin: 8; Layout.bottomMargin: 8 }
                    Label { text: qsTr("录制设置"); color: window.ink; font.pixelSize: 17; font.bold: true }
                    RowLayout {
                        Layout.fillWidth: true
                        ColumnLayout { Layout.fillWidth: true; Label { text: qsTr("文件名（不分段时使用）") } TextField { id: editFileName; Layout.fillWidth: true; placeholderText: qsTr("留空则使用 1") } }
                        ColumnLayout { Layout.preferredWidth: 190; Label { text: qsTr("检测间隔（秒）") } TextField { id: editInterval; Layout.fillWidth: true; validator: IntValidator { bottom: 30; top: 86400 } } }
                    }
                    Label { text: qsTr("保存目录") }
                    RowLayout { Layout.fillWidth: true; TextField { id: editRoot; Layout.fillWidth: true } AppButton { text: qsTr("选择目录"); onClicked: { const value = desktopActions.chooseDirectory(editRoot.text); if (value.length > 0) editRoot.text = value } } }
                    Label { text: qsTr("代理地址（可选）") }
                    TextField { id: editProxy; Layout.fillWidth: true; placeholderText: qsTr("例如 127.0.0.1:7890；留空表示直连") }
                    RowLayout {
                        Layout.fillWidth: true
                        ColumnLayout { Layout.fillWidth: true; Label { text: qsTr("录制清晰度") } ComboBox { id: editQuality; model: window.qualityOptions; textRole: "text"; valueRole: "value"; Layout.fillWidth: true } }
                        ColumnLayout { Layout.fillWidth: true; Label { text: qsTr("录制路线") } ComboBox { id: editLine; model: window.lineOptions; textRole: "text"; valueRole: "value"; Layout.fillWidth: true } }
                    }
                    RowLayout {
                        Layout.fillWidth: true
                        ColumnLayout { Layout.fillWidth: true; Label { text: qsTr("输出格式") } ComboBox { id: editFormat; model: ["ts", "mp4", "mkv", "flv", "mp3", "m4a"]; Layout.fillWidth: true } }
                        ColumnLayout { Layout.fillWidth: true; Label { text: qsTr("分段时长（分钟）") } RowLayout { Layout.fillWidth: true; CheckBox { id: editSegment; text: qsTr("启用") } TextField { id: editMinutes; Layout.fillWidth: true; enabled: editSegment.checked; validator: IntValidator { bottom: 1; top: 1440 } } } }
                    }
                    Label { text: qsTr("分段文件固定按 1、2、3… 排列，最后一段按实际剩余时长保存。"); color: window.muted; font.pixelSize: 11 }
                    CheckBox { id: editConvert; text: qsTr("录制完成后转为 MP4（成功后删除 TS）"); enabled: editFormat.currentText === "ts" && !editAudio.checked }
                    CheckBox { id: editAudio; text: qsTr("纯音频模式") }
                    CheckBox { id: editDanmaku; text: qsTr("录制弹幕（仅在平台适配完成后生效）") }
                }
            }
            Label { visible: editDialog.errorText.length > 0; text: editDialog.errorText; color: window.danger; Layout.fillWidth: true; wrapMode: Text.Wrap }
            Rectangle { Layout.fillWidth: true; Layout.preferredHeight: 1; color: window.lineColor }
            RowLayout {
                Layout.fillWidth: true; Item { Layout.fillWidth: true }
                AppButton { text: qsTr("取消"); onClicked: editDialog.close() }
                AppButton {
                    text: qsTr("保存"); tone: "primary"
                    onClicked: { const error = roomModel.updateRoom(editDialog.roomId, editName.text, editTitle.text, editUrl.text, editFileName.text, editInterval.text, editRoot.text, editProxy.text, editFormat.currentText, editQuality.currentValue, editLine.currentValue, editSegment.checked, editMinutes.text, editConvert.checked, editAudio.checked, editDanmaku.checked); if (error.length > 0) editDialog.errorText = error; else { editDialog.close(); window.operationMessage = qsTr("直播间设置已保存") } }
                }
            }
        }
    }

    Dialog {
        id: deleteAllDialog
        title: qsTr("删除全部直播间"); modal: true; anchors.centerIn: parent; width: 470
        background: Rectangle { color: window.surface; radius: 16; border.width: 1; border.color: window.lineColor }
        property string errorText: ""
        onOpened: errorText = ""
        ColumnLayout {
            width: parent.width; spacing: 14
            Label { text: qsTr("确定从 Reco Box 中删除全部直播间吗？\n录制文件和历史记录不会删除。"); wrapMode: Text.Wrap; Layout.fillWidth: true }
            Label { visible: deleteAllDialog.errorText.length > 0; text: deleteAllDialog.errorText; color: window.danger; wrapMode: Text.Wrap; Layout.fillWidth: true }
            RowLayout { Layout.fillWidth: true; Item { Layout.fillWidth: true } AppButton { text: qsTr("取消"); onClicked: deleteAllDialog.close() } AppButton { text: qsTr("确认全部删除"); tone: "dangerSolid"; onClicked: { const error = roomModel.removeAllRooms(); if (error.length > 0) deleteAllDialog.errorText = error; else { deleteAllDialog.close(); window.operationMessage = qsTr("已删除全部直播间") } } } }
        }
    }

    Dialog {
        id: globalDialog
        title: qsTr("全局设置"); modal: true; anchors.centerIn: parent; width: 940; height: 680
        standardButtons: Dialog.Close
        background: Rectangle { color: window.surface; radius: 16; border.width: 1; border.color: window.lineColor }
        ColumnLayout {
            anchors.fill: parent; spacing: 10
            TabBar { id: globalTabs; Layout.fillWidth: true; TabButton { text: qsTr("全局设置") } TabButton { text: qsTr("录制历史"); onClicked: historyModel.refresh() } TabButton { text: qsTr("运行日志"); onClicked: eventLogModel.refresh() } }
            StackLayout {
                Layout.fillWidth: true; Layout.fillHeight: true; currentIndex: globalTabs.currentIndex
                ScrollView {
                    clip: true; ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                    ColumnLayout {
                        width: globalDialog.availableWidth - 30; spacing: 11
                        RowLayout { Layout.fillWidth: true; Label { text: qsTr("新直播间默认设置"); color: window.ink; font.pixelSize: 17; font.weight: Font.DemiBold } Item { Layout.fillWidth: true } AppButton { text: qsTr("导入旧配置"); onClicked: legacyDialog.open() } }
                        Label { text: qsTr("界面语言") }
                        ComboBox {
                            id: languageSelector; Layout.fillWidth: true
                            model: localizationController.languages; textRole: "name"; valueRole: "code"
                            currentIndex: window.optionIndex(model, localizationController.currentLanguage)
                            onActivated: {
                                if (localizationController.setLanguage(currentValue)) {
                                    window.settingsMessage = qsTr("界面语言已切换")
                                }
                            }
                        }
                        Label { text: qsTr("只影响以后新增或导入的直播间；已有直播间在卡片中单独编辑。"); color: window.muted; font.pixelSize: 11 }
                        Label { text: qsTr("默认录制目录") }
                        RowLayout { Layout.fillWidth: true; TextField { id: defaultRootField; text: settingsController.defaultSaveRoot; Layout.fillWidth: true } AppButton { text: qsTr("选择目录"); onClicked: { const value = desktopActions.chooseDirectory(defaultRootField.text); if (value.length > 0) defaultRootField.text = value } } }
                        RowLayout {
                            Layout.fillWidth: true
                            ColumnLayout { Layout.fillWidth: true; Label { text: qsTr("默认格式") } ComboBox { id: defaultFormat; model: ["ts", "mp4", "mkv", "flv", "mp3", "m4a"]; currentIndex: Math.max(0, model.indexOf(settingsController.defaultOutputFormat)); Layout.fillWidth: true } }
                            ColumnLayout { Layout.fillWidth: true; Label { text: qsTr("默认画质") } ComboBox { id: defaultQuality; model: window.qualityOptions; textRole: "text"; valueRole: "value"; currentIndex: window.optionIndex(model, settingsController.defaultQuality); Layout.fillWidth: true } }
                            ColumnLayout { Layout.preferredWidth: 170; Label { text: qsTr("检测间隔（秒）") } TextField { id: defaultInterval; text: String(settingsController.defaultCheckInterval); validator: IntValidator { bottom: 30; top: 86400 } Layout.fillWidth: true } }
                            ColumnLayout { Layout.preferredWidth: 170; Label { text: qsTr("磁盘保护（GB）") } TextField { id: minimumFreeGb; text: String(settingsController.minimumFreeGb); validator: IntValidator { bottom: 1; top: 1024 } Layout.fillWidth: true } }
                        }
                        Label { text: qsTr("Resolver 调度限制"); color: window.ink; font.pixelSize: 15; font.weight: Font.DemiBold }
                        RowLayout {
                            Layout.fillWidth: true
                            ColumnLayout { Layout.fillWidth: true; Label { text: qsTr("最大并发") } TextField { id: resolverMaxConcurrency; text: String(settingsController.resolverMaxConcurrency); validator: IntValidator { bottom: 1; top: 32 } Layout.fillWidth: true } }
                            ColumnLayout { Layout.fillWidth: true; Label { text: qsTr("单平台并发") } TextField { id: resolverPlatformConcurrency; text: String(settingsController.resolverPlatformConcurrency); validator: IntValidator { bottom: 1; top: 16 } Layout.fillWidth: true } }
                            ColumnLayout { Layout.fillWidth: true; Label { text: qsTr("平台冷却（秒）") } TextField { id: resolverPlatformInterval; text: String(settingsController.resolverPlatformIntervalSeconds); validator: IntValidator { bottom: 0; top: 3600 } Layout.fillWidth: true } }
                        }
                        Label { text: qsTr("用于分散解析请求；修改后立即影响新的监控请求。"); color: window.muted; font.pixelSize: 11 }
                        Label { text: qsTr("默认代理地址（可选）") }
                        TextField { id: defaultProxy; text: settingsController.defaultProxy; Layout.fillWidth: true; placeholderText: qsTr("新直播间继承；留空表示直连") }
                        CheckBox { id: defaultSegment; text: qsTr("新直播间默认启用分段"); checked: settingsController.defaultSegmentEnabled; onClicked: window.settingsMessage = qsTr("设置已更改，请点击保存设置") }
                        RowLayout { enabled: defaultSegment.checked; Label { text: qsTr("每段") } TextField { id: defaultSegmentMinutes; text: String(settingsController.defaultSegmentMinutes); Layout.preferredWidth: 100; validator: IntValidator { bottom: 1; top: 1440 } onTextEdited: window.settingsMessage = qsTr("设置已更改，请点击保存设置") } Label { text: qsTr("分钟，最后一段按实际时长保存"); color: window.muted } }
                        RowLayout {
                            Layout.fillWidth: true
                            Label { text: qsTr("启动后自动监控 · 关闭窗口最小化到托盘 · 不随 Windows 开机启动"); color: window.muted; font.pixelSize: 11 }
                            Item { Layout.fillWidth: true }
                            AppButton { text: qsTr("保存设置"); tone: "primary"; onClicked: { const error = settingsController.saveDefaults(defaultRootField.text, defaultFormat.currentText, defaultQuality.currentValue, defaultInterval.text, defaultSegment.checked, defaultSegmentMinutes.text, minimumFreeGb.text, defaultProxy.text, resolverMaxConcurrency.text, resolverPlatformConcurrency.text, resolverPlatformInterval.text); window.settingsMessage = error.length > 0 ? error : (defaultSegment.checked ? qsTr("已保存并确认：以后新增直播间默认每 ") + defaultSegmentMinutes.text + qsTr(" 分钟分段") : qsTr("已保存并确认：以后新增直播间默认不分段")) } }
                        }
                        Label { text: window.settingsMessage; color: window.settingsMessage.indexOf(qsTr("已保存并确认")) === 0 ? window.success : window.settingsMessage.indexOf(qsTr("设置已更改")) === 0 ? window.warning : window.danger; font.pixelSize: 11; font.weight: Font.DemiBold }
                    }
                }
                ListView {
                    clip: true; spacing: 8; model: historyModel
                    delegate: Rectangle {
                        required property var streamer_name; required property var started_at; required property var ended_at; required property var status; required property var total_bytes; required property var error_message; required property var session_dirs; required property var probe_status; required property var duration_seconds; required property var codec_summary
                        width: ListView.view.width; height: 92; radius: 12; color: window.surfaceSubtle; border.width: 1; border.color: "#ECEEF1"
                        RowLayout {
                            anchors.fill: parent; anchors.margins: 13
                            ColumnLayout { Layout.fillWidth: true; Label { text: streamer_name; color: window.ink; font.weight: Font.DemiBold } Label { text: started_at + (ended_at ? " — " + ended_at : ""); color: window.muted; font.pixelSize: 10 } Label { text: codec_summary + (Number(duration_seconds) > 0 ? " · " + window.durationText(Math.round(Number(duration_seconds))) : ""); color: window.muted; font.pixelSize: 10 } Label { visible: String(error_message).length > 0; text: error_message; color: window.danger; font.pixelSize: 10; elide: Text.ElideRight; Layout.fillWidth: true } }
                            Label { text: window.bytesText(Number(total_bytes)); color: window.muted }
                            Label { text: probe_status === "valid" ? qsTr("可播放") : status === "converting" ? qsTr("转 MP4 中") : status === "recording" ? qsTr("录制中") : status === "completed" ? qsTr("已完成") : qsTr("失败"); color: probe_status === "valid" || status === "completed" ? window.success : window.ink; font.weight: Font.DemiBold }
                            AppButton { text: qsTr("播放"); compact: true; enabled: status !== "recording" && status !== "converting"; onClicked: desktopActions.playRecording(String(session_dirs)) }
                            AppButton { text: qsTr("目录"); compact: true; enabled: status !== "recording" && status !== "converting"; onClicked: desktopActions.openRecordingDirectories(String(session_dirs)) }
                        }
                    }
                }
                ColumnLayout {
                    Label { text: qsTr("这里只显示脱敏后的状态和错误，不保存完整临时播放地址。"); color: window.muted; font.pixelSize: 11 }
                    ListView {
                        Layout.fillWidth: true; Layout.fillHeight: true; clip: true; spacing: 8; model: eventLogModel
                        delegate: Rectangle {
                            required property var streamer_name; required property var level; required property var message; required property var created_at
                            width: ListView.view.width; height: 66; radius: 12; color: window.surfaceSubtle; border.width: 1; border.color: "#ECEEF1"
                            RowLayout { anchors.fill: parent; anchors.margins: 12; Rectangle { Layout.preferredWidth: 8; Layout.preferredHeight: 8; radius: 4; color: level === "error" ? window.danger : window.success } ColumnLayout { Layout.fillWidth: true; Label { text: streamer_name + " · " + created_at; color: window.muted; font.pixelSize: 10 } Label { text: message; color: window.ink; font.pixelSize: 11; elide: Text.ElideRight; Layout.fillWidth: true } } }
                        }
                    }
                }
            }
        }
    }

    Dialog {
        id: previewDialog
        title: previewController.title; modal: false; anchors.centerIn: parent; width: 900; height: 560; standardButtons: Dialog.Close
        background: Rectangle { color: window.surface; radius: 16; border.width: 1; border.color: window.lineColor }
        onClosed: { previewPlayer.stop(); previewController.clear() }
        MediaPlayer {
            id: previewPlayer
            source: previewController.source
            audioOutput: AudioOutput { volume: 0.8 }
            videoOutput: previewVideo
            onErrorOccurred: function(error, errorString) {
                previewController.setPlayerError(errorString.length > 0 ? errorString : qsTr("直播流播放失败"))
            }
            onMediaStatusChanged: {
                if (mediaStatus === MediaPlayer.InvalidMedia)
                    previewController.setPlayerError(qsTr("直播流格式无效或播放器无法解码"))
            }
        }
        Connections { target: previewController; function onChanged() { if (previewController.source.toString().length > 0) previewPlayer.play() } }
        ColumnLayout {
            anchors.fill: parent
            Rectangle {
                Layout.fillWidth: true; Layout.fillHeight: true; color: "#111111"; radius: 10
                VideoOutput { id: previewVideo; anchors.fill: parent; fillMode: VideoOutput.PreserveAspectFit }
                Column {
                    anchors.centerIn: parent; spacing: 12
                    BusyIndicator {
                        anchors.horizontalCenter: parent.horizontalCenter
                        running: previewController.source.toString().length > 0 && !previewPlayer.hasVideo && previewController.error.length === 0
                        visible: running
                    }
                    Label {
                        anchors.horizontalCenter: parent.horizontalCenter
                        width: Math.min(620, parent.parent.width - 80)
                        horizontalAlignment: Text.AlignHCenter; wrapMode: Text.Wrap
                        visible: previewController.error.length > 0 || !previewPlayer.hasVideo
                        text: previewController.error.length > 0
                            ? previewController.error
                            : previewController.source.toString().length === 0
                                ? qsTr("正在准备预览……")
                                : qsTr("正在连接直播流并等待首帧……")
                        color: previewController.error.length > 0 ? "#FF9B9B" : "white"
                    }
                }
            }
            RowLayout { Layout.fillWidth: true; Label { text: previewController.error; color: window.danger; elide: Text.ElideRight; Layout.fillWidth: true } AppButton { text: previewPlayer.playbackState === MediaPlayer.PlayingState ? qsTr("暂停") : qsTr("播放"); tone: "primary"; enabled: previewController.source.toString().length > 0; onClicked: previewPlayer.playbackState === MediaPlayer.PlayingState ? previewPlayer.pause() : previewPlayer.play() } AppButton { text: qsTr("静音"); checkable: true; onToggled: previewPlayer.audioOutput.muted = checked } }
        }
    }

    Dialog {
        id: legacyDialog
        title: qsTr("导入 DouyinLiveRecorder 旧配置"); modal: true; anchors.centerIn: parent; width: 640; standardButtons: Dialog.Close
        background: Rectangle { color: window.surface; radius: 16; border.width: 1; border.color: window.lineColor }
        ColumnLayout {
            width: parent.width; spacing: 10
            Label { text: qsTr("选择旧程序根目录或其中的 config 文件夹。") }
            RowLayout { Layout.fillWidth: true; TextField { id: legacyFolderField; Layout.fillWidth: true } AppButton { text: qsTr("选择文件夹"); onClicked: { const value = desktopActions.chooseDirectory(legacyFolderField.text); if (value.length > 0) legacyFolderField.text = value } } }
            RowLayout { AppButton { text: qsTr("1. 预检"); enabled: legacyFolderField.text.length > 0; onClicked: legacyImport.preview(legacyFolderField.text) } AppButton { text: qsTr("2. 确认导入"); tone: "primary"; enabled: legacyImport.previewText.indexOf(qsTr("可导入直播间")) >= 0; onClicked: legacyImport.runImport(legacyFolderField.text) } }
            ScrollView { Layout.fillWidth: true; Layout.preferredHeight: 250; TextArea { readOnly: true; text: legacyImport.resultText.length > 0 ? legacyImport.resultText : legacyImport.previewText; wrapMode: Text.Wrap } }
            Label { text: qsTr("不会修改旧配置；Cookie、令牌、账号、密码和推送凭据不会导入。"); color: window.muted; font.pixelSize: 11 }
        }
    }
}

