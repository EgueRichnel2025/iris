import QtQuick
import QtQuick3D
import QtQuick3D.AssetUtils
Item {
    id: root
    width: 1280
    height: 720
    property url frameSource: ""
    property url modelSource: ""
    property vector3d facePosition: Qt.vector3d(0, 0, -30)
    property vector3d faceEulerRotation: Qt.vector3d(0, 0, 0)
    property bool hasFace: false
    property bool glassesEnabled: false
    property bool modelLoaded: glassesModel.status === RuntimeLoader.Success
    property string modelError: glassesModel.errorString
    Image { id: cameraImage; anchors.fill: parent; source: root.frameSource; fillMode: Image.PreserveAspectFit; cache: false; asynchronous: false }
    View3D {
        anchors.centerIn: cameraImage
        width: cameraImage.paintedWidth
        height: cameraImage.paintedHeight
        environment: SceneEnvironment { backgroundMode: SceneEnvironment.Transparent }
        camera: PerspectiveCamera { position: Qt.vector3d(0, 0, 0); fieldOfView: 43.6; clipNear: 0.1; clipFar: 300 }
        DirectionalLight { eulerRotation: Qt.vector3d(-20, -20, 0); brightness: 1.0 }
        RuntimeLoader {
            id: glassesModel
            source: root.modelSource
            position: root.facePosition
            eulerRotation: root.faceEulerRotation
            scale: Qt.vector3d(88, 88, 88)
            visible: root.glassesEnabled && root.hasFace && status === RuntimeLoader.Success
        }
    }
}
