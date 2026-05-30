import React, { useState, useMemo } from 'react';

// Mock Data structure representing stocks with Open, High, Low, Close (OHLC) values
const ALL_STOCKS_DATA = [
  { id: 1, name: "Tata Consultancy Services Ltd.", symbol: "TCS", open: 3850, high: 3890, low: 3840, close: 3851, volume: "1.2M" },
  { id: 2, name: "Reliance Industries Ltd.", symbol: "RELIANCE", open: 2450, high: 2480, low: 2410, close: 2450.5, volume: "3.4M" },
  { id: 3, name: "Infosys Ltd.", symbol: "INFY", open: 1420, high: 1460, low: 1410, close: 1455, volume: "2.1M" }, // Not a Doji
  { id: 4, name: "HDFC Bank Ltd.", symbol: "HDFCBANK", open: 1510, high: 1530, low: 1505, close: 1511, volume: "4.8M" },
  { id: 5, name: "Wipro Ltd.", symbol: "WIPRO", open: 420, high: 435, low: 418, close: 432, volume: "950K" }, // Not a Doji
  { id: 6, name: "State Bank of India", symbol: "SBIN", open: 780, high: 795, low: 778, close: 780.2, volume: "6.1M" },
];

export default function DojiScreener() {
  const [timeframe, setTimeframe] = useState('1D');
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: 'symbol', direction: 'ascending' });

  // 1. Technical Screening Logic (Doji Equation Implementation)
  const screenedStocks = useMemo(() => {
    return ALL_STOCKS_DATA.filter(stock => {
      const body = Math.abs(stock.open - stock.close);
      const totalRange = stock.high - stock.low;
      
      // Doji Condition: Candle body must be less than or equal to 10% of total day range
      const isDoji = body <= (totalRange * 0.10);
      
      // Simulate variations across timeframes just for ui/demonstration purposes
      if (timeframe === '1W' && stock.id === 1) return false;
      if (timeframe === '1M' && stock.id === 2) return false;

      return isDoji;
    });
  }, [timeframe]);

  // 2. Global Searching / Filtering Logic
  const filteredStocks = useMemo(() => {
    return screenedStocks.filter(stock => 
      stock.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      stock.symbol.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [screenedStocks, searchTerm]);

  // 3. Sorting Logic
  const sortedStocks = useMemo(() => {
    let sortableItems = [...filteredStocks];
    if (sortConfig !== null) {
      sortableItems.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [filteredStocks, sortConfig]);

  const requestSort = (key) => {
    let direction = 'ascending';
    if (sortConfig && sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  // Calculate percentage change for placeholder visualization
  const getPctChange = (stock) => {
    const chg = ((stock.close - stock.open) / stock.open) * 100;
    return chg.toFixed(2);
  };

  return (
    <div className="w-full max-w-6xl mx-auto px-4 py-8 text-white">
      {/* Timeframe Selectors Header */}
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold mb-4">Doji Screener</h2>
        <div className="flex justify-center gap-2">
          {['1D', '1W', '1M', '3M'].map((tf) => (
            <button
              key={tf}
              onClick={() => setTimeframe(tf)}
              className={`px-4 py-2 text-sm font-semibold rounded border transition-colors ${
                timeframe === tf 
                  ? 'bg-white text-black border-white' 
                  : 'bg-transparent text-white border-gray-600 hover:bg-gray-800'
              }`}
            >
              {tf}
            </button>
          ))}
        </div>
      </div>

      {/* Dynamic Data Table Area */}
      <div className="bg-[#0d1117] border border-gray-800 rounded-lg p-6 shadow-xl">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4 mb-6">
          <div>
            <h3 className="text-lg font-semibold">Scan Results</h3>
            <p className="text-sm text-gray-400">Showing {sortedStocks.length} stocks matching Doji criteria ({timeframe})</p>
          </div>
          
          <div className="flex gap-3 w-full sm:w-auto">
            <input 
              type="text"
              placeholder="Search stock..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-[#161b22] border border-gray-700 rounded px-3 py-1.5 text-sm w-full sm:w-64 focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>

        {sortedStocks.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm border-collapse">
              <thead>
                <tr className="bg-[#161b22] text-gray-400 uppercase text-xs border-b border-gray-800">
                  <th className="py-3 px-4 w-16">Sr.</th>
                  <th onClick={() => requestSort('name')} className="py-3 px-4 cursor-pointer hover:text-white select-none">
                    Stock Name {sortConfig.key === 'name' ? (sortConfig.direction === 'ascending' ? '▲' : '▼') : ''}
                  </th>
                  <th onClick={() => requestSort('symbol')} className="py-3 px-4 cursor-pointer hover:text-white select-none">
                    Symbol {sortConfig.key === 'symbol' ? (sortConfig.direction === 'ascending' ? '▲' : '▼') : ''}
                  </th>
                  <th onClick={() => requestSort('close')} className="py-3 px-4 cursor-pointer hover:text-white select-none text-right">
                    Price {sortConfig.key === 'close' ? (sortConfig.direction === 'ascending' ? '▲' : '▼') : ''}
                  </th>
                  <th className="py-3 px-4 text-right">Chg %</th>
                  <th onClick={() => requestSort('volume')} className="py-3 px-4 cursor-pointer hover:text-white select-none text-right">
                    Volume {sortConfig.key === 'volume' ? (sortConfig.direction === 'ascending' ? '▲' : '▼') : ''}
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800">
                {sortedStocks.map((stock, index) => {
                  const change = getPctChange(stock);
                  return (
                    <tr key={stock.id} className="hover:bg-[#1f242c] transition-colors group">
                      <td className="py-3.5 px-4 text-gray-500">{index + 1}</td>
                      <td className="py-3.5 px-4 font-medium text-gray-200 group-hover:text-white">{stock.name}</td>
                      <td className="py-3.5 px-4 text-blue-400 font-bold hover:underline cursor-pointer">{stock.symbol}</td>
                      <td className="py-3.5 px-4 text-right font-mono font-medium">₹{stock.close.toLocaleString()}</td>
                      <td className={`py-3.5 px-4 text-right font-mono font-semibold ${Number(change) >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                        {Number(change) >= 0 ? `+${change}%` : `${change}%`}
                      </td>
                      <td className="py-3.5 px-4 text-right font-mono text-gray-400">{stock.volume}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500 border border-dashed border-gray-800 rounded">
            No stocks found matching the Doji criteria for this period.
          </div>
        )}
      </div>
    </div>
  );
}
