import React, { useState, useMemo } from 'react';

const DominionCalculator = () => {
  const [deckSize, setDeckSize] = useState('');
  const [labCount, setLabCount] = useState('');
  const [singleResult, setSingleResult] = useState('');
  const [tableResult, setTableResult] = useState([]);
  const [maxDeckSize, setMaxDeckSize] = useState('');
  const [maxLabCount, setMaxLabCount] = useState('');
  const [isCalculating, setIsCalculating] = useState(false);

  const simulateDraw = (deckSize, labCount) => {
    const deck = Array(deckSize).fill(0).fill(1, 0, labCount);
    let hand = [], playArea = [];
    
    for (let i = 0; i < 5 && deck.length > 0; i++) {
      const randomIndex = Math.floor(Math.random() * deck.length);
      hand.push(deck.splice(randomIndex, 1)[0]);
    }
    
    while (hand.length > 0) {
      const card = hand.pop();
      playArea.push(card);
      if (card === 1) {
        for (let i = 0; i < 2 && deck.length > 0; i++) {
          const randomIndex = Math.floor(Math.random() * deck.length);
          hand.push(deck.splice(randomIndex, 1)[0]);
        }
      }
    }
    
    return deck.length === 0;
  };

  const calculateProbability = (deckSize, labCount, simulations = 10000) => {
    let successCount = 0;
    for (let i = 0; i < simulations; i++) {
      if (simulateDraw(deckSize, labCount)) successCount++;
    }
    return successCount / simulations;
  };

  const calculateSingle = () => {
    setIsCalculating(true);
    setTimeout(() => {
      const probability = calculateProbability(parseInt(deckSize), parseInt(labCount));
      setSingleResult(`引き切り確率: ${(probability * 100).toFixed(2)}%`);
      setIsCalculating(false);
    }, 0);
  };

  const calculateTable = () => {
    setIsCalculating(true);
    setTimeout(() => {
      const data = [];
      for (let d = 10; d <= parseInt(maxDeckSize); d++) {
        const row = [{ deck_size: d }];
        for (let l = 0; l <= parseInt(maxLabCount); l++) {
          row.push({ draw_probability: calculateProbability(d, l) });
        }
        data.push(row);
      }
      setTableResult(data);
      setIsCalculating(false);
    }, 0);
  };

  const getColorForProbability = (probability) => {
    const r = Math.round(255 * (1 - probability));
    const g = Math.round(255 * probability);
    return `rgb(${r}, ${g}, 0)`;
  };

  const tableHeader = useMemo(() => {
    if (tableResult.length === 0) return null;
    return (
      <tr>
        <th className="border p-2 bg-gray-100">デッキ枚数</th>
        {Array.from({ length: parseInt(maxLabCount) + 1 }, (_, i) => (
          <th key={i} className="border p-2 bg-gray-100">研究所{i}枚</th>
        ))}
      </tr>
    );
  }, [maxLabCount, tableResult]);

  const typicalProbabilities = [
    { deckSize: 10, labCounts: [0, 1, 2, 3] },
    { deckSize: 15, labCounts: [0, 1, 2, 3, 4] },
    { deckSize: 20, labCounts: [0, 1, 2, 3, 4, 5] },
    { deckSize: 25, labCounts: [0, 1, 2, 3, 4, 5, 6] },
    { deckSize: 30, labCounts: [0, 1, 2, 3, 4, 5, 6, 7] },
  ];

  return (
    <div className="max-w-6xl mx-auto bg-white rounded-xl shadow-md overflow-hidden p-6">
      <h1 className="text-3xl font-bold mb-6 text-center text-indigo-600">ドミニオン デッキ引き切り確率計算機</h1>
      
      <div className="mb-8 bg-gray-50 p-4 rounded-lg">
        <h2 className="text-2xl font-semibold mb-4 text-indigo-500">単一計算</h2>
        <div className="flex flex-wrap gap-4 mb-4">
          <input
            type="number"
            placeholder="デッキ枚数"
            value={deckSize}
            onChange={(e) => setDeckSize(e.target.value)}
            className="flex-1 border p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <input
            type="number"
            placeholder="研究所枚数"
            value={labCount}
            onChange={(e) => setLabCount(e.target.value)}
            className="flex-1 border p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <button 
          onClick={calculateSingle} 
          disabled={isCalculating}
          className="w-full bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition duration-200 ease-in-out"
        >
          {isCalculating ? '計算中...' : '計算'}
        </button>
        <p className="mt-4 text-lg font-semibold text-center">{singleResult}</p>
      </div>

      <div className="bg-gray-50 p-4 rounded-lg mb-8">
        <h2 className="text-2xl font-semibold mb-4 text-indigo-500">確率表生成</h2>
        <div className="flex flex-wrap gap-4 mb-4">
          <input
            type="number"
            placeholder="最大デッキ枚数"
            value={maxDeckSize}
            onChange={(e) => setMaxDeckSize(e.target.value)}
            className="flex-1 border p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <input
            type="number"
            placeholder="最大研究所枚数"
            value={maxLabCount}
            onChange={(e) => setMaxLabCount(e.target.value)}
            className="flex-1 border p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <button 
          onClick={calculateTable}
          disabled={isCalculating}
          className="w-full bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition duration-200 ease-in-out"
        >
          {isCalculating ? '計算中...' : '表を生成'}
        </button>
        {tableResult.length > 0 && (
          <div className="mt-6 overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-300">
              <thead>{tableHeader}</thead>
              <tbody>
                {tableResult.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {row.map((cell, cellIndex) => (
                      <td 
                        key={cellIndex} 
                        className="border p-2 text-center"
                        style={cellIndex !== 0 ? { backgroundColor: getColorForProbability(cell.draw_probability) } : {}}
                      >
                        {cell.deck_size || `${(cell.draw_probability * 100).toFixed(2)}%`}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="bg-gray-50 p-4 rounded-lg">
        <h2 className="text-2xl font-semibold mb-4 text-indigo-500">典型的な確率表</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border border-gray-300">
            <thead>
              <tr>
                <th className="border p-2 bg-gray-100">デッキ枚数</th>
                {typicalProbabilities[0].labCounts.map((_, index) => (
                  <th key={index} className="border p-2 bg-gray-100">研究所{index}枚</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {typicalProbabilities.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  <td className="border p-2 text-center">{row.deckSize}</td>
                  {row.labCounts.map((labCount, index) => {
                    const probability = calculateProbability(row.deckSize, labCount);
                    return (
                      <td 
                        key={index} 
                        className="border p-2 text-center"
                        style={{ backgroundColor: getColorForProbability(probability) }}
                      >
                        {(probability * 100).toFixed(2)}%
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DominionCalculator;
