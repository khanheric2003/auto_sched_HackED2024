import createEngine, {
  DiagramModel,
  DefaultNodeModel,
} from "@projectstorm/react-diagrams";

import { CanvasWidget } from "@projectstorm/react-diagrams";

function App() {
  let engine = createEngine();
  let model = new DiagramModel();
  //3-A) create a default node
  let node1 = new DefaultNodeModel({
    name: "CMPUT 174",
    color: "rgb(0,192,255)",
  });
  node1.setPosition(100, 100);
  let port1 = node1.addOutPort("Out");

  //3-B) create another default node
  let node2 = new DefaultNodeModel("CMPUT 175", "rgb(192,255,0)");
  let port2 = node2.addInPort("In");
  node2.setPosition(400, 100);

  // link the ports
  let link1 = port1.link(port2);
  link1.getOptions().testName = "Test";
  link1.addLabel("Hello World!");

  //4) add the models to the root graph
  model.addAll(node1, node2, link1);

  //5) load model into engine
  engine.setModel(model);
  return (
    <CanvasWidget className="h-screen bg-slate-700" engine={engine} />
  );
}

export default App;
