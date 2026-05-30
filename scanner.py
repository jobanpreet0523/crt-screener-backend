import React, { useState, useEffect, useMemo } from 'react';

export default function DojiScreener() {
  // State Matrix
  const [timeframe, setTimeframe] = useState('1D'); // UI state tracking (uppercase)
  const [liveStocksData, setLiveStocksData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: 'symbol', direction: 'ascending' });
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState(null);

  // Define API Production Server Base URI - Update this when your Render instance goes live!
  const BASE_API_URL = "https://crt-screener-backend-1.onrender.com";

  // Asynchronous Effect Engine calling your exact `/scan` route
  useEffect(() => {
    const fetchLiveData = async () => {
      setIsLoading(true);
      setApiError(null);
      
      // Convert UI Timeframe state to match the lowercase keys expected by tf_params in main.py
      const backendTf = timeframe.toLowerCase();

      try {
        // Querying your universal scan endpoint using 'doji' filter parameters
        const response = await fetch(`${BASE_API_URL}/scan?type=doji&tf=${backendTf}&market=NSE&limit=30`);
        
        if (!response.ok) {
          throw new Error(`Server returned error status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.ok && data.results) {
          setLiveStocksData(data.results);
        } else {
          setLiveStocksData([]);
        }
      } catch (err) {
        console.error("FastAPI connection failure:", err);
        setApiError("Unable to connect to trading backend engine. Ensure Uvicorn is active on port 8000.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchLiveData();
  }, [timeframe]); // Fires instantly whenever the user clicks a different timeframe button

  // 1. Client-Side Global Search Filtering 
  const filteredStocks = useMemo(() => {
    return liveStocksData.filter(stock => 
      stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (stock.sector && stock.sector.toLowerCase().includes(searchTerm.toLowerCase()))
    );
  }, [liveStocksData, searchTerm]);

  // 2. Client-Side Column Sorting Engine Matrix
  const sortedStocks = useMemo(() => {
    let sortableItems = [...filteredStocks];
    if (sortConfig !== null) {
      sortableItems.sort((a, b) => {
        let valA = a[sortConfig.key];
        let valB = b[sortConfig.key];

        // Safe Fallbacks handling numeric float conversions 
        if (typeof valA === 'string') {
          return sortConfig.direction === 'ascending' 
            ? valA.localeCompare(valB) 
            : valB.localeCompare(valA);
        } else {
          return sortConfig.direction === 'ascending' ? valA - valB : valB - valA;
        }
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
            <p className="text-sm text-gray-400">
              {isLoading ? "Running technical calculations..." : `Showing ${sortedStocks.length} live matching assets (${timeframe})`}
            </p>
          </div>
          
          <div className="flex gap-3 w-full sm:w-auto">
            <input 
              type="text"
              placeholder="Search ticker or sector..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-[#161b22] border border-gray-700 rounded px-3 py-1.5 text-sm w-full sm:w-64 focus:outline-none focus:border-blue-500 text-white"
            />
          </div>
        </div>

        {/* State Conditional Renders */}
        {apiError && (
          <div className="text-center py-6 px-4 mb-4 bg-red-950/40 border border-red-900 text-red-400 rounded-md text-sm font-mono">
            {apiError}
          </div>
        )}

        {isLoading ? (
          <div className="text-center py-20 text-blue-400 font-mono text-sm animate-pulse">
            Fetching active OHLC data matrices from Yahoo Finance pipeline...
          </div>
        ) : sortedStocks.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm border-collapse">
              <thead>
                <tr className="bg-[#161b22] text-gray-400 uppercase text-xs border-b border-gray-800">
                  <th className="py-3 px-4 w-16">Sr.</th>
                  <th onClick={() => requestSort('symbol')} className="py-3 px-4 cursor-pointer hover:text-white select-none">
                    Ticker {sortConfig.key === 'symbol' ? (sortConfig.direction === 'ascending' ? '▲' : '▼') : ''}
                  </th>
                  <th onClick={() => requestSort('sector')} className="py-3 px-4 cursor-pointer hover:text-white select-none">
                    Sector {sortConfig.key === 'sector' ? (sortConfig.direction === 'ascending' ? '▲' : '▼') : ''}
                  </th>
                  <th onClick={() => requestSort('price')} className="py-3 px-4 cursor-pointer hover:text-white select-none text-right">
                    Price {sortConfig.key === 'price' ? (sortConfig.direction === 'ascending' ? '▲' : '▼') : ''}
                  </th>
                  <th onClick={() => requestSort('change')} className="py-3 px-4 cursor-pointer hover:text-white select-none text-right">
                    Chg % {sortConfig.key === 'change' ? (sortConfig.direction === 'ascending' ? '▲' : '▼') : ''}
                  </th>
                  <th onClick={() => requestSort('volume')} className="py-3 px-4 cursor-pointer hover:text-white select-none text-right">
                    Volume {sortConfig.key === 'volume' ? (sortConfig.direction === 'ascending' ? '▲' : '▼') : ''}
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800">
                {sortedStocks.map((stock, index) => {
                  return (
                    <tr key={stock.symbol} className="hover:bg-[#1f242c] transition-colors group">
                      <td className="py-3.5 px-4 text-gray-500 font-mono">{index + 1}</td>
                      <td className="py-3.5 px-4 text-blue-400 font-bold hover:underline cursor-pointer">
                        <a 
                          href={`https://finance.yahoo.com/quote/${stock.symbol}.NS`} 
                          target="_blank" 
                          rel="noreferrer"
                        >
                          {stock.symbol}
                        </a>
                      </td>
                      <td className="py-3.5 px-4 text-gray-300 font-medium">{stock.sector || "Other"}</td>
                      <td className="py-3.5 px-4 text-right font-mono font-medium text-gray-100">
                        ₹{stock.price.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                      </td>
                      <td className={`py-3.5 px-4 text-right font-mono font-semibold ${stock.change >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                        {stock.change >= 0 ? `+${stock.change}%` : `${stock.change}%`}
                      </td>
                      <td className="py-3.5 px-4 text-right font-mono text-gray-400">
                        {(stock.volume / 100000).toFixed(1)} L
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-16 text-gray-500 border border-dashed border-gray-800 rounded">
            No live equities match the processing criteria for this period right now.
          </div>
        )}
      </div>
    </div>
  );
}
