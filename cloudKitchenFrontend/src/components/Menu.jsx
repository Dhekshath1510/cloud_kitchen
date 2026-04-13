import React from 'react'
import AnimatedButton from './AnimatedButton'
import vegIcon from '../icons/veg-icon.png'
import nonVegIcon from '../icons/non-veg-icon.png'

const PLACEHOLDER_IMAGE = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="300" height="200"%3E%3Crect width="300" height="200" fill="%23e0e0e0"/%3E%3Ctext x="50%25" y="50%25" font-size="16" text-anchor="middle" dy=".3em" fill="%23999"%3ENo Image%3C/text%3E%3C/svg%3E'

const Menu = ({ menu, onAdd }) => {
  return (
    <div>
        <ul className='p-5 grid grid-cols-3 gap-3 shadow-md rounded-[10px]'>
            {menu && menu.map((item, idx)=>(
                <li key={idx} className='flex flex-col gap-3 shadow-md'>
                    <img 
                      src={item.imageUrl || PLACEHOLDER_IMAGE} 
                      alt={item.itemName} 
                      className='w-full h-48 object-cover rounded-[10px]'
                      onError={(e) => { e.target.src = PLACEHOLDER_IMAGE }}
                    />
                    <div className='flex flex-row justify-between items-center px-2'>
                        <h2 className='font-bold text-lg'>{item.itemName}</h2>
                        <span className='text-sm text-gray-500'>
                            {item.isVeg ? 
                            <img src={vegIcon} alt="Veg icon" className='h-5 w-5'></img> : 
                            <img src={nonVegIcon} alt='Non Veg icon' className='h-5 w-5'></img>}
                        </span>
                    </div>
                    <p className='text-sm text-gray-600 px-2'>{item.description}</p>
                    <div className='mt-auto flex flex-row justify-between items-center px-2'>
                        <span className='font-semibold text-md'>Rs.{item.price}</span>
                        <AnimatedButton variant="primary" className="mb-2 px-2 py-1 mt-3 text-sm" onClick={() => onAdd && onAdd(item)}>Add</AnimatedButton>
                    </div>
                </li>
            ))}
        </ul>
    </div>
  )
}

export default Menu