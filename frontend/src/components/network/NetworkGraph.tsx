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
 position: {
 x: 0,
 y: 0,
 },

 data: {
 label: network.name || network.person_id,
 },

 style: {
 background:"#2563eb",
 color:"#ffffff",
 border:"1px solid #60a5fa",
 borderRadius: 12,
 padding: 12,
 width: 180,
 fontWeight: 600,
 },
 });


 network.connections.forEach((connection, index) => {

 const angle =
 (2 * Math.PI * index) /
 Math.max(network.connections.length, 1);

 const radius = 300;


 nodes.push({
 id: connection.id,

 position: {
 x: Math.cos(angle) * radius,
 y: Math.sin(angle) * radius,
 },

 data: {
 label: connection.name || connection.id,
 },

 style: {
 background:"#111827",
 color:"#cbd5e1",
 border:"1px solid #334155",
 borderRadius: 10,
 padding: 10,
 width: 150,
 },
 });


 edges.push({
 id: `${network.person_id}-${connection.id}-${index}`,

 source: network.person_id,

 target: connection.id,

 label: connection.relationship,

 animated: false,

 style: {
 stroke:"#475569",
 },

 labelStyle: {
 fill:"#94a3b8",
 fontSize: 10,
 },
 });

 });


 return {
 nodes,
 edges,
 };
}


export default function NetworkGraph({
 network,
}: Props) {

 const {
 nodes,
 edges,
 } = buildGraph(network);


 return (
 <div className="h-[650px] overflow-hidden border border-white/10 bg-[#080d18]">

 <ReactFlow
 nodes={nodes}
 edges={edges}
 fitView
 proOptions={{
 hideAttribution: true,
 }}
 >

 <Background />

 <Controls />

 <MiniMap />

 </ReactFlow>

 </div>
 );
}