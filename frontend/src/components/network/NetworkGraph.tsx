import {
 Background,
 Controls,
 MiniMap,
 ReactFlow,
 type Edge,
 type Node,
} from"reactflow";

import"reactflow/dist/style.css";

import type {
 PersonNetwork,
} from"../../types/person";


interface Props {
 network: PersonNetwork;
}


function buildGraph(network: PersonNetwork) {

 const nodes: Node[] = [];
 const edges: Edge[] = [];


  nodes.push({
    id: network.person_id,
    position: { x: 0, y: 0 },
    data: { label: network.name || network.person_id },
    style: {
      background: "var(--color-primary)",
      color: "var(--color-primary-foreground)",
      border: "1px solid var(--color-primary)",
      borderRadius: 0,
      padding: 12,
      width: 180,
      fontWeight: 600,
      fontFamily: "monospace",
      boxShadow: "0 0 15px rgba(0,255,65,0.4)",
    },
  });

  network.connections.forEach((connection, index) => {
    const angle = (2 * Math.PI * index) / Math.max(network.connections.length, 1);
    const radius = 300;

    nodes.push({
      id: connection.id,
      position: {
        x: Math.cos(angle) * radius,
        y: Math.sin(angle) * radius,
      },
      data: { label: connection.name || connection.id },
      style: {
        background: "var(--color-background)",
        color: "var(--color-primary)",
        border: "1px solid var(--color-primary)",
        borderRadius: 0,
        padding: 10,
        width: 150,
        fontFamily: "monospace",
      },
    });

    edges.push({
      id: `${network.person_id}-${connection.id}-${index}`,
      source: network.person_id,
      target: connection.id,
      label: connection.relationship,
      animated: false,
      style: { stroke: "var(--color-primary)", opacity: 0.5 },
      labelStyle: { fill: "var(--color-primary)", fontSize: 10, fontFamily: "monospace" },
    });
  });

  return { nodes, edges };
}

export default function NetworkGraph({ network }: Props) {
  const { nodes, edges } = buildGraph(network);

  return (
    <div className="h-[650px] overflow-hidden bg-[var(--color-card)] border-t border-[var(--color-primary)]/20">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        proOptions={{ hideAttribution: true }}
      >
        <Background color="rgba(0,255,65,0.15)" gap={20} size={1} />
        <Controls className="bg-[var(--color-background)] border-[var(--color-primary)]/50 fill-[var(--color-primary)] rounded-none overflow-hidden" />
        <MiniMap 
          nodeColor={(node) => node.id === network.person_id ? "var(--color-primary)" : "var(--color-muted)"} 
          maskColor="var(--color-card)"
          className="bg-[var(--color-background)] border-[var(--color-primary)]/50 rounded-none"
        />
      </ReactFlow>
    </div>
  );
}