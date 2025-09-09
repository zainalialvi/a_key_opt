import streamlit as st
import openai

openai.api_key = st.secrets["idrak_gpt_key"]
# Function to call GPT and generate optimized title
def fun_gpt_choose_title_and_rearrange_it(user_prompt):
    system_prompt = '''
    You are an Alibaba SEO and product growth expert specializing in optimizing product titles 
    to boost search visibility and sales performance. Your expertise ensures that the final 
    output is concise, keyword-rich, and tailored to attract buyers while maintaining the 
    integrity of the product description.
    '''

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1
    )

    refined_product_name = response['choices'][0]['message']['content'].strip()
    return refined_product_name


# ------------------ Streamlit UI ------------------
st.title("Alibaba Product Title Optimizer")

# Old title input
old_product_title = st.text_input("Enter Old Product Title")

# Raw product titles input (multi-line)
raw_titles_input = st.text_area("Enter Raw Product Titles (one per line)")

# Convert input to list
raw_product_list = [line.strip() for line in raw_titles_input.split("\n") if line.strip()]

# Pre-filled editable prompt
default_prompt = f'''
Your task is to optimize an Alibaba product title. Follow these steps carefully for precise, SEO-optimized, and highly relevant results:

1. **Old Product Title**:  
   - Character Length: {len(old_product_title)}  
   - Title: "{old_product_title}"  

2. **Suggested Product Titles**:  
   - Titles: {raw_product_list}  
   - Character Lengths of Titles accordingly: {[len(prod_title) for prod_title in raw_product_list]}

### Guidelines for Title Optimization:
3. **Selection Criteria**:  
   a. Choose the best title from the list based on:  
      - Alignment with the product's core features in the old title.  
      - Retention of critical keywords and product-specific details like "Set of 5", "Collection of", "3.5 Inch Nail Scissor", or "6 Inch Scissors".  
      - High keyword density relevant to Alibaba SEO practices.  
      - Clarity and readability for potential buyers.  

4. **Rearrangement and Optimization**:  
   a. Once the best title is selected:  
      - Retain all critical keywords from both the old and new titles.  
      - Arrange the title for maximum clarity and engagement.  
      - Avoid unnecessary filler words while ensuring the title remains professional.  

   b. Character Length Adjustments:  
      - Ensure the final title is concise and within **100 to 110 characters**.  
      - If the optimized title is below 100 characters, add relevant keywords to reach at least 100 characters.  
      - Under no circumstances should the title exceed **110 characters**.  

   c. Additions and Edits:  
      - Any added keywords must enhance SEO and relevance while maintaining the meaning and clarity of the title.  
      - Avoid special characters like commas, dashes, or semicolons.  

### Output Requirements:  
5. **Final Title**:  
   - Return only the fully optimized title as a single string.  
   - The title must be professional, SEO-friendly, and aligned with the product's core features.  
   - Do not include explanations, notes, or additional text in the response.  
'''

user_prompt = st.text_area("Edit Prompt (Optional)", value=default_prompt, height=400)

# Generate button
if st.button("Generate Optimized Title"):
    if old_product_title and raw_product_list:
        # Fill dynamic values in the prompt
        filled_prompt = user_prompt.format(
            old_product_title=old_product_title,
            raw_product_list=raw_product_list
        )
        final_title = fun_gpt_choose_title_and_rearrange_it(filled_prompt)

        st.subheader("Results")
        st.write(f"**Old Title:** {old_product_title}")
        st.write(f"**Generated Title:** {final_title}")
    else:
        st.warning("⚠️ Please enter both an old product title and raw product titles.")
