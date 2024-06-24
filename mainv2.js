import React, { useState, useMemo } from 'react';

const DominionCalculator = () => {
  const [deckSize, setDeckSize] = useState('10');
  const [drawCards, setDrawCards] = useState([1,2,3,4,5].map(draw => ({ draw, count: 0 })));
  const [singleResult, setSingleResult] = useState('');
  const [tableResult, setTableResult] = useState([]);
  const [maxDeckSize, setMaxDeckSize] = useState('30');
  const [selectedDrawCard, setSelectedDrawCard] = useState(2);
  const [maxDrawCardCount, setMaxDrawCardCount] = useState('5');
  const [isCalculating, setIsCalculating] = useState(false);

  const simulateDraw = (deckSize, drawCards) => {
    let deck = Array(deckSize).fill(0);
    drawCards.forEach(card => deck.fill(card.draw, 0, card.count));
    deck.sort(() => Math.random() - 0.5);
    
    let hand = deck.splice(0, 5);
    while (hand.length > 0) {
      const card = hand.pop();
      hand.push(...deck.splice(0, card));
    }
    
    return deck.length === 0;
  };

  const calculateProbability = (deckSize, drawCards, simulations = 10000) => 
    Array(simulations).fill().filter(() => simulateDraw(deckSize, drawCards)).length / simulations;

  const handleDrawCardChange = (index, value) => 
    setDrawCards(cards => cards.map((card, i) => i === index ? { ...card, count: parseInt(value) || 0 } : card));

  const calculate = (singleCalc = true) => {
    setIsCalculating(true);
    setTimeout(() => {
      if (singleCalc) {
        const probability = calculateProbability(parseInt(deckSize), drawCards);
        setSingleResult(`引き切り確率: ${(probability * 100).toFixed(2)}%`);
      } else {
        const data = Array.from({length: parseInt(maxDeckSize) - 9}, (_, i) => i + 10).map(d => {
          const row = [{ deck_size: d }];
          for (let c = 0; c <= parseInt(maxDrawCardCount); c++) {
            const tempDrawCards = drawCards.map(card => 
              card.draw === selectedDrawCard ? { ...card, count: c } : card
            );
            row.push({ draw_probability: calculateProbability(d, tempDrawCards) });
          }
          return row;
        });
        setTableResult(data);
      }
      setIsCalculating(false);
    }, 0);
  };

  const getColorForProbability = (probability) => 
    `rgb(${Math.round(255 * (1 - probability))}, ${Math.round(255 * probability)}, 0)`;

  const tableHeader = useMemo(() => 
    tableResult.length > 0 && (
      <tr>
        <th className="border p-2 bg-gray-100">デッキ枚数</th>
        {Array.from({ length: parseInt(maxDrawCardCount) + 1 }, (_, i) => (
          <th key={i} className="border p-2 bg-gray-100">ドロー{selectedDrawCard} {i}枚</th>
        ))}
      </tr>
    ), [maxDrawCardCount, selectedDrawCard, tableResult]);

  return (
    <div className="max-w-6xl mx-auto bg-white rounded-xl shadow-md overflow-hidden p-6">
      <h1 className="text-3xl font-bold mb-6 text-center text-indigo-600">ドミニオン デッキ引き切り確率計算機</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-gray-50 p-4 rounded-lg">
          <h2 className="text-2xl font-semibold mb-4 text-indigo-500">単一計算</h2>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">デッキ枚数</label>
              <input
                type="number"
                value={deckSize}
                onChange={(e) => setDeckSize(e.target.value)}
                className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            {drawCards.map((card, index) => (
              <div key={index}>
                <label className="block text-sm font-medium text-gray-700 mb-1">ドロー{card.draw}</label>
                <input
                  type="number"
                  value={card.count}
                  onChange={(e) => handleDrawCardChange(index, e.target.value)}
                  className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            ))}
          </div>
          <button 
            onClick={() => calculate()}
            disabled={isCalculating}
            className="w-full bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition duration-200 ease-in-out"
          >
            {isCalculating ? '計算中...' : '計算'}
          </button>
          <p className="mt-4 text-lg font-semibold text-center">{singleResult}</p>
        </div>

        <div className="bg-gray-50 p-4 rounded-lg">
          <h2 className="text-2xl font-semibold mb-4 text-indigo-500">確率表生成</h2>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">最大デッキ枚数</label>
              <input
                type="number"
                value={maxDeckSize}
                onChange={(e) => setMaxDeckSize(e.target.value)}
                className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">最大ドロー枚数</label>
              <input
                type="number"
                value={maxDrawCardCount}
                onChange={(e) => setMaxDrawCardCount(e.target.value)}
                className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">対象ドローカード</label>
              <select
                value={selectedDrawCard}
                onChange={(e) => setSelectedDrawCard(parseInt(e.target.value))}
                className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                {drawCards.map(card => (
                  <option key={card.draw} value={card.draw}>ドロー{card.draw}</option>
                ))}
              </select>
            </div>
          </div>
          <button 
            onClick={() => calculate(false)}
            disabled={isCalculating}
            className="w-full bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition duration-200 ease-in-out"
          >
            {isCalculating ? '計算中...' : '表を生成'}
          </button>
        </div>
      </div>

      {tableResult.length > 0 && (
        <div className="mt-8 overflow-x-auto">
          <table className="min-w-full bg-white border border-gray-300">
            <thead>{tableHeader}</thead>
            <tbody>
              {tableResult.map((row, rowIndex) => (
                <tr key={rowIndex} className={rowIndex % 2 === 0 ? 'bg-gray-50' : ''}>
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

      <div className="mt-8 text-sm text-gray-600">
        <h3 className="font-semibold mb-2">使い方：</h3>
        <ol className="list-decimal list-inside space-y-1">
          <li>単一計算：デッキ枚数と各ドローカードの枚数を入力し、「計算」をクリックします。</li>
          <li>確率表生成：最大デッキ枚数、最大ドロー枚数、対象ドローカードを選択し、「表を生成」をクリックします。</li>
          <li>表の色：緑に近いほど引き切り確率が高く、赤に近いほど低いことを示します。</li>
        </ol>
      </div>
    </div>
  );
};

export default DominionCalculator;
