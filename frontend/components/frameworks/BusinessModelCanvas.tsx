"use client"

interface BusinessModelCanvasData {
  key_partners: string
  key_activities: string
  key_resources: string
  value_propositions: string
  customer_relationships: string
  channels: string
  customer_segments: string
  cost_structure: string
  revenue_streams: string
}

interface BusinessModelCanvasProps {
  data: BusinessModelCanvasData
}

export default function BusinessModelCanvas({ data }: BusinessModelCanvasProps) {
  if (!data) {
    return <div className="text-red-500">Canvas 데이터가 없습니다.</div>
  }
  
  return (
    <div className="w-full max-w-6xl mx-auto my-4">
      <h3 className="text-lg font-bold mb-4 text-gray-800">Business Model Canvas</h3>
      <div className="grid grid-cols-10 border border-gray-300 bg-white">
        {/* Row 1 & 2: Top Section */}
        
        {/* Key Partners - Leftmost, Tall (2 cols, 2 rows) */}
        <div className="col-span-2 row-span-2 bg-blue-50 border-r border-b border-gray-300 p-4">
          <h3 className="text-xs font-bold uppercase text-gray-500 mb-2">KEY PARTNERS</h3>
          <div className="text-gray-700 whitespace-pre-wrap text-xs leading-relaxed overflow-y-auto max-h-[200px]">
            {data.key_partners || "입력 필요"}
          </div>
        </div>
        
        {/* Key Activities - 2nd col, top (2 cols, 1 row) */}
        <div className="col-span-2 bg-green-50 border-r border-b border-gray-300 p-4">
          <h3 className="text-xs font-bold uppercase text-gray-500 mb-2">KEY ACTIVITIES</h3>
          <div className="text-gray-700 whitespace-pre-wrap text-xs leading-relaxed overflow-y-auto max-h-[100px]">
            {data.key_activities || "입력 필요"}
          </div>
        </div>
        
        {/* Value Propositions - Center, Tall (2 cols, 2 rows) */}
        <div className="col-span-2 row-span-2 bg-purple-50 border-r border-b border-gray-300 p-4">
          <h3 className="text-xs font-bold uppercase text-gray-500 mb-2">VALUE PROPOSITIONS</h3>
          <div className="text-gray-700 whitespace-pre-wrap text-xs leading-relaxed overflow-y-auto max-h-[200px]">
            {data.value_propositions || "입력 필요"}
          </div>
        </div>
        
        {/* Customer Relationships - 4th col, top (2 cols, 1 row) */}
        <div className="col-span-2 bg-orange-50 border-r border-b border-gray-300 p-4">
          <h3 className="text-xs font-bold uppercase text-gray-500 mb-2">CUSTOMER RELATIONSHIPS</h3>
          <div className="text-gray-700 whitespace-pre-wrap text-xs leading-relaxed overflow-y-auto max-h-[100px]">
            {data.customer_relationships || "입력 필요"}
          </div>
        </div>
        
        {/* Customer Segments - Rightmost, Tall (2 cols, 2 rows) */}
        <div className="col-span-2 row-span-2 bg-indigo-50 border-b border-gray-300 p-4">
          <h3 className="text-xs font-bold uppercase text-gray-500 mb-2">CUSTOMER SEGMENTS</h3>
          <div className="text-gray-700 whitespace-pre-wrap text-xs leading-relaxed overflow-y-auto max-h-[200px]">
            {data.customer_segments || "입력 필요"}
          </div>
        </div>
        
        {/* Key Resources - 2nd col, bottom (2 cols, 1 row) */}
        <div className="col-span-2 bg-yellow-50 border-r border-b border-gray-300 p-4">
          <h3 className="text-xs font-bold uppercase text-gray-500 mb-2">KEY RESOURCES</h3>
          <div className="text-gray-700 whitespace-pre-wrap text-xs leading-relaxed overflow-y-auto max-h-[100px]">
            {data.key_resources || "입력 필요"}
          </div>
        </div>
        
        {/* Channels - 4th col, bottom (2 cols, 1 row) */}
        <div className="col-span-2 bg-pink-50 border-r border-b border-gray-300 p-4">
          <h3 className="text-xs font-bold uppercase text-gray-500 mb-2">CHANNELS</h3>
          <div className="text-gray-700 whitespace-pre-wrap text-xs leading-relaxed overflow-y-auto max-h-[100px]">
            {data.channels || "입력 필요"}
          </div>
        </div>
        
        {/* Row 3: Bottom Section */}
        
        {/* Cost Structure - Bottom Left (5 cols) */}
        <div className="col-span-5 bg-red-50 border-r border-b border-gray-300 p-4">
          <h3 className="text-xs font-bold uppercase text-gray-500 mb-2">COST STRUCTURE</h3>
          <div className="text-gray-700 whitespace-pre-wrap text-xs leading-relaxed overflow-y-auto max-h-[150px]">
            {data.cost_structure || "입력 필요"}
          </div>
        </div>
        
        {/* Revenue Streams - Bottom Right (5 cols) */}
        <div className="col-span-5 bg-teal-50 border-b border-gray-300 p-4">
          <h3 className="text-xs font-bold uppercase text-gray-500 mb-2">REVENUE STREAMS</h3>
          <div className="text-gray-700 whitespace-pre-wrap text-xs leading-relaxed overflow-y-auto max-h-[150px]">
            {data.revenue_streams || "입력 필요"}
          </div>
        </div>
      </div>
    </div>
  )
}
