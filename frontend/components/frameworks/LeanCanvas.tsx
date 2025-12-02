"use client"

interface LeanCanvasData {
  problem: string
  solution: string
  unique_value_prop: string
  unfair_advantage: string
  customer_segments: string
  key_metrics: string
  channels: string
  cost_structure: string
  revenue_streams: string
}

interface LeanCanvasProps {
  data: LeanCanvasData
}

export default function LeanCanvas({ data }: LeanCanvasProps) {
  if (!data) {
    return <div className="text-red-500">Canvas 데이터가 없습니다.</div>
  }
  
  return (
    <div className="w-full my-4 overflow-x-auto">
      <h3 className="text-lg font-bold mb-4 text-gray-800">Lean Canvas</h3>
      <div className="grid grid-cols-10 border-2 border-gray-400 bg-white gap-0 min-w-[1000px]">
        {/* Row 1 & 2: Top Section with 5 vertical columns */}
        
        {/* 1. Problem - Leftmost, col-span-2 row-span-2 (Tall) */}
        <div className="col-span-2 row-span-2 p-4 border-r-2 border-b-2 border-gray-400 min-h-[200px] bg-blue-50">
          <h3 className="text-xs font-bold uppercase text-gray-600 mb-2">PROBLEM</h3>
          <div className="text-sm text-gray-900 whitespace-pre-wrap leading-relaxed">
            {data.problem || "입력 필요"}
          </div>
        </div>
        
        {/* 2. Solution - 2nd col, top, col-span-2 (Short) */}
        <div className="col-span-2 p-4 border-r-2 border-b-2 border-gray-400 min-h-[100px] bg-green-50">
          <h3 className="text-xs font-bold uppercase text-gray-600 mb-2">SOLUTION</h3>
          <div className="text-sm text-gray-900 whitespace-pre-wrap leading-relaxed">
            {data.solution || "입력 필요"}
          </div>
        </div>
        
        {/* 3. Unique Value Proposition - Center, col-span-2 row-span-2 (Tall) */}
        <div className="col-span-2 row-span-2 p-4 border-r-2 border-b-2 border-gray-400 min-h-[200px] bg-yellow-50">
          <h3 className="text-xs font-bold uppercase text-gray-600 mb-2">UNIQUE VALUE PROPOSITION</h3>
          <div className="text-sm text-gray-900 whitespace-pre-wrap leading-relaxed">
            {data.unique_value_prop || "입력 필요"}
          </div>
        </div>
        
        {/* 4. Unfair Advantage - 4th col, top, col-span-2 (Short) */}
        <div className="col-span-2 p-4 border-r-2 border-b-2 border-gray-400 min-h-[100px] bg-purple-50">
          <h3 className="text-xs font-bold uppercase text-gray-600 mb-2">UNFAIR ADVANTAGE</h3>
          <div className="text-sm text-gray-900 whitespace-pre-wrap leading-relaxed">
            {data.unfair_advantage || "입력 필요"}
          </div>
        </div>
        
        {/* 5. Customer Segments - Rightmost, col-span-2 row-span-2 (Tall) */}
        <div className="col-span-2 row-span-2 p-4 border-b-2 border-gray-400 min-h-[200px] bg-orange-50">
          <h3 className="text-xs font-bold uppercase text-gray-600 mb-2">CUSTOMER SEGMENTS</h3>
          <div className="text-sm text-gray-900 whitespace-pre-wrap leading-relaxed">
            {data.customer_segments || "입력 필요"}
          </div>
        </div>
        
        {/* Row 2 continuation: Key Metrics and Channels */}
        
        {/* 6. Key Metrics - 2nd col, bottom, col-span-2 (Short) */}
        <div className="col-span-2 p-4 border-r-2 border-b-2 border-gray-400 min-h-[100px] bg-pink-50">
          <h3 className="text-xs font-bold uppercase text-gray-600 mb-2">KEY METRICS</h3>
          <div className="text-sm text-gray-900 whitespace-pre-wrap leading-relaxed">
            {data.key_metrics || "입력 필요"}
          </div>
        </div>
        
        {/* 7. Channels - 4th col, bottom, col-span-2 (Short) */}
        <div className="col-span-2 p-4 border-r-2 border-b-2 border-gray-400 min-h-[100px] bg-indigo-50">
          <h3 className="text-xs font-bold uppercase text-gray-600 mb-2">CHANNELS</h3>
          <div className="text-sm text-gray-900 whitespace-pre-wrap leading-relaxed">
            {data.channels || "입력 필요"}
          </div>
        </div>
        
        {/* Row 3: Bottom Section - Cost Structure and Revenue Streams */}
        
        {/* 8. Cost Structure - Bottom Left, col-span-5 (Wide, half width) */}
        <div className="col-span-5 p-4 border-r-2 border-b-2 border-gray-400 min-h-[120px] bg-red-50">
          <h3 className="text-xs font-bold uppercase text-gray-600 mb-2">COST STRUCTURE</h3>
          <div className="text-sm text-gray-900 whitespace-pre-wrap leading-relaxed">
            {data.cost_structure || "입력 필요"}
          </div>
        </div>
        
        {/* 9. Revenue Streams - Bottom Right, col-span-5 (Wide, half width) */}
        <div className="col-span-5 p-4 border-b-2 border-gray-400 min-h-[120px] bg-teal-50">
          <h3 className="text-xs font-bold uppercase text-gray-600 mb-2">REVENUE STREAMS</h3>
          <div className="text-sm text-gray-900 whitespace-pre-wrap leading-relaxed">
            {data.revenue_streams || "입력 필요"}
          </div>
        </div>
      </div>
    </div>
  )
}
