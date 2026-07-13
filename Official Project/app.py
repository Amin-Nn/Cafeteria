from flask import Flask, render_template, request, jsonify
from PDataBase import get_db_connection

app = Flask(__name__)


CAFETERIA_INFO = {
    'name': 'Campus Cafeteria',
    'phone': '(555) 123-4567',
    'email': 'cafeteria@campus.edu',
    'hours': 'Mon-Fri: 7AM-7PM | Sat-Sun: 10AM-5PM',
    'location': 'Building A, Floor 1'
}

@app.route('/')
def home():
    """Home/Cover page with cafeteria info and links"""
    return render_template('index.html', page=1, cafeteria_info=CAFETERIA_INFO)

@app.route('/menu/<int:page_num>')
def menu(page_num):
    """Display menu page"""
    if page_num < 1 or page_num > 5:
        return "Page not found", 404
    
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM menu_items WHERE page = ?', (page_num,)).fetchall()
    conn.close()
    
    page_titles = {
        1: 'Home',
        2: 'Breakfast',
        3: 'Lunch',
        4: 'Snacks & Beverages',
        5: 'Desserts'
    }
    
    return render_template('index.html', 
                          page=page_num, 
                          items=items, 
                          page_title=page_titles.get(page_num, 'Menu'),
                          cafeteria_info=CAFETERIA_INFO)

@app.route('/api/ratings', methods=['GET'])
def get_ratings():
    """Get ratings for items"""
    item_id = request.args.get('item_id', type=int)
    conn = get_db_connection()
    ratings = conn.execute('SELECT AVG(rating) as avg_rating, COUNT(*) as count FROM ratings WHERE item_id = ?', 
                          (item_id,)).fetchone()
    conn.close()
    return jsonify({
        'avg_rating': ratings['avg_rating'] or 0,
        'count': ratings['count'] or 0
    })

@app.route('/api/ratings', methods=['POST'])
def submit_rating():
    """Submit a rating for an item"""
    data = request.get_json()
    item_id = data.get('item_id')
    rating = data.get('rating')
    comment = data.get('comment', '')
    
    if not (1 <= rating <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    conn = get_db_connection()
    conn.execute('INSERT INTO ratings (item_id, rating, comment) VALUES (?, ?, ?)',
                (item_id, rating, comment))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Rating submitted!'})

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit general feedback"""
    data = request.get_json()
    name = data.get('name', 'Anonymous')
    email = data.get('email', '')
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    conn = get_db_connection()
    conn.execute('INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)',
                (name, email, message))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Thank you for your feedback!'})

if __name__ == '__main__':
    app.run(debug=True)